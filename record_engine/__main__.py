"""Command line.

python -m record_engine observe  [--documents documents] [--out .local/record_engine]
python -m record_engine build    [--out ...]            # observations -> record, abstraction.*
python -m record_engine ask      --questions FILE [--ids DEV-01 ...] [--gate DEV-01..05] [--out ...]
python -m record_engine add      FILE ... [--workspace DIR]  # copy into a workspace, re-observe, rebuild, diff
                                  # (the supplied documents/ folder is never written to)
python -m record_engine diff     --before A.json [--after B.json]
python -m record_engine trace    ID                                  # fact or event -> sources
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Any

from record_engine import llm, render
from record_engine.ingest import ingest_folder
from record_engine.policy import load


def run_observe(documents: Any, policy: Any, args: argparse.Namespace) -> None:
    from record_engine.crosscheck import observe_checked
    from record_engine.pipeline import write_jsonl

    started = time.monotonic()
    observations, problems, report = observe_checked(documents, policy, args.workers)
    write_jsonl(args.out / "observations.jsonl", observations)
    write_jsonl(args.out / "extraction_issues.jsonl", problems)
    per_document = report.pop("per_document")
    summary = {
        "run": {"usage": llm.USAGE.as_dict(), "seconds": round(time.monotonic() - started, 1)},
        "crosscheck": report,
        "per_document": per_document,
    }
    (args.out / "extraction_stats.json").write_text(json.dumps(summary, indent=1))
    print(
        json.dumps(
            {
                "documents": len(documents),
                "observations": len(observations),
                "issues": len(problems),
                "unextracted_mentions": sum(p.kind == "unextracted_mention" for p in problems),
                "reading_disagreements": report["disagreements"],
                "settled_by_reread": report["settled"],
                "left_open": report["open"],
                "seconds": round(time.monotonic() - started, 1),
                "usage": llm.USAGE.as_dict(),
            }
        )
    )


def run_build(documents: Any, policy: Any, args: argparse.Namespace) -> Any:
    from record_engine.model import OpenItem
    from record_engine.pipeline import read_observations
    from record_engine.reconcile import build_record
    from record_engine.render import abstraction_markdown

    observations = read_observations(args.out / "observations.jsonl")
    issues_path = args.out / "extraction_issues.jsonl"
    issues = (
        [OpenItem.model_validate_json(x) for x in issues_path.read_text().splitlines() if x]
        if issues_path.exists()
        else []
    )
    record = build_record(documents, observations, policy, issues)
    (args.out / "abstraction.json").write_text(record.model_dump_json(indent=1))
    (args.out / "abstraction.md").write_text(abstraction_markdown(record, documents))
    print(
        json.dumps(
            {
                "events": len(record.events),
                "facts": len(record.facts),
                "open_items": len(record.open_items),
            }
        )
    )
    return record


def expand_ids(items: list[str]) -> list[str]:
    """DEV-01..05 -> DEV-01 ... DEV-05 (keeps the zero padding); plain IDs pass through."""
    out: list[str] = []
    for item in items:
        m = re.fullmatch(r"(.*?)(\d+)\.\.(\d+)", item)
        if not m:
            out.append(item)
            continue
        prefix, first, last = m.groups()
        out += [f"{prefix}{n:0{len(first)}d}" for n in range(int(first), int(last) + 1)]
    return out


def gate_failures(answers_path: Path, gate: list[str]) -> list[str]:
    """Gated questions that are missing or withheld."""
    if not gate:
        return []
    answers = {a["id"]: a for a in json.loads(answers_path.read_text())}
    return [q for q in gate if answers.get(q, {}).get("status") in (None, "withheld")]


def main() -> None:
    parser = argparse.ArgumentParser(prog="record_engine")
    parser.add_argument("command", choices=["observe", "build", "ask", "add", "diff", "trace"])
    parser.add_argument("targets", nargs="*", help="files for add; an ID for trace")
    parser.add_argument("--before", type=Path)
    parser.add_argument("--after", type=Path)
    parser.add_argument("--documents", type=Path, default=Path("documents"))
    parser.add_argument("--out", type=Path, default=Path(".local/record_engine"))
    parser.add_argument("--policy", type=str, default=None)
    parser.add_argument("--questions", type=Path)
    parser.add_argument("--ids", nargs="*")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="for add: folder holding a working copy of the documents (default OUT/workspace)",
    )
    parser.add_argument(
        "--gate",
        nargs="*",
        default=[],
        help="question IDs (or a range like DEV-01..05) that must be published; exit 1 otherwise",
    )
    args = parser.parse_args()
    policy = load(args.policy)
    documents = ingest_folder(args.documents)
    # Markdown outputs link to the source documents relative to where they are written.
    render.DOCUMENTS_BASE = os.path.relpath(args.documents.resolve(), args.out.resolve())
    args.out.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()

    if args.command == "add":
        import shutil

        from record_engine.changes import diff, diff_markdown
        from record_engine.model import Record

        previous = args.out / "abstraction.json"
        before = Record.model_validate_json(previous.read_text()) if previous.exists() else None
        # new documents go into a working copy, never into the supplied documents folder
        workspace = (args.workspace or args.out / "workspace") / "documents"
        if not workspace.exists():
            shutil.copytree(args.documents, workspace)
        for name in args.targets:
            shutil.copy(name, workspace / Path(name).name)
        documents = ingest_folder(workspace)
        # abstraction.md links to the working copy, which holds the added documents
        render.DOCUMENTS_BASE = os.path.relpath(workspace.resolve(), args.out.resolve())
        print(json.dumps({"workspace": str(workspace), "documents": len(documents)}))
        run_observe(documents, policy, args)
        record = run_build(documents, policy, args)
        if before is not None:
            changes = diff(before, record)
            (args.out / "abstraction.prev.json").write_text(before.model_dump_json(indent=1))
            (args.out / "changes.json").write_text(json.dumps(changes, indent=1))
            (args.out / "changes.md").write_text(diff_markdown(changes))
            print(diff_markdown(changes))
        return
    if args.command == "diff":
        from record_engine.changes import diff, diff_markdown
        from record_engine.model import Record

        before = Record.model_validate_json(args.before.read_text())
        after = Record.model_validate_json(
            (args.after or args.out / "abstraction.json").read_text()
        )
        print(diff_markdown(diff(before, after)))
        return
    if args.command == "trace":
        from record_engine.changes import trace
        from record_engine.model import Record
        from record_engine.pipeline import read_observations

        record = Record.model_validate_json((args.out / "abstraction.json").read_text())
        observations = read_observations(args.out / "observations.jsonl")
        for target in args.targets:
            print(trace(target, record, observations, documents))
        return
    if args.command == "observe":
        run_observe(documents, policy, args)
    elif args.command == "build":
        run_build(documents, policy, args)
    else:
        from record_engine.qa import ask_all

        ask_all(documents, policy, args.out, args.questions, args.ids, args.workers)
        print(
            json.dumps(
                {"usage": llm.USAGE.as_dict(), "seconds": round(time.monotonic() - started, 1)}
            )
        )
        failed = gate_failures(args.out / "answers.json", expand_ids(args.gate))
        if failed:
            print(json.dumps({"gate": "failed", "not_published": failed}))
            raise SystemExit(1)


if __name__ == "__main__":
    main()
