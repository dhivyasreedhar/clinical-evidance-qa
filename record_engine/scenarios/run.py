"""End-to-end scenario tests: new wording and formats, changed inputs, and new questions.

Each scenario copies the supplied documents into its own workspace, adds or removes documents,
re-runs extraction (unchanged documents come from the cache), rebuilds the record, checks the
record deterministically, answers its questions and checks each answer. Nothing is written to
documents/.

    python -m record_engine.scenarios.run                    # all scenarios
    python -m record_engine.scenarios.run --only S01 S04     # some
    python -m record_engine.scenarios.run --judge            # also grade answers with the
                                                             # benchmark judge (one more call each)

Record checks and answer checks are deterministic; the judge is advisory. Output:
.local/scenarios/report.md and report.json.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import time
from pathlib import Path
from typing import Any

from record_engine import llm
from record_engine.ingest import ingest_folder
from record_engine.model import Record
from record_engine.policy import Policy, load

HERE = Path(__file__).parent
TOTAL = "from encounters where disposition = included select count(), count_distinct(date), sum(minutes)"
WEEKS = (
    "from encounters where disposition = included group_by week "
    "select count_distinct(date), sum(minutes), goal_met()"
)


def workspace(scenario: dict[str, Any], documents: Path, root: Path) -> Path:
    folder: Path = root / str(scenario["id"]) / "documents"
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    removed = scenario.get("remove", [])
    for path in sorted(documents.glob("*.txt")):
        if not any(path.stem.startswith(r) for r in removed):
            shutil.copy(path, folder / path.name)
    for name in scenario.get("add", []):
        shutil.copy(HERE / "docs" / name, folder / name)
    return folder


def build(folder: Path, policy: Policy, out: Path, workers: int) -> tuple[Record, list[Any]]:
    from record_engine.crosscheck import observe_checked
    from record_engine.pipeline import write_jsonl
    from record_engine.reconcile import build_record
    from record_engine.render import abstraction_markdown

    documents = ingest_folder(folder)
    observations, problems, _report = observe_checked(documents, policy, workers)
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "observations.jsonl", observations)
    record = build_record(documents, observations, policy, problems)
    (out / "abstraction.json").write_text(record.model_dump_json(indent=1))
    (out / "abstraction.md").write_text(abstraction_markdown(record, documents))
    return record, documents


def _scenarios(value: Any) -> list[float]:
    if isinstance(value, dict) and "scenarios" in value:
        return sorted(float(v) for v in value["scenarios"])
    if isinstance(value, (int, float)):
        return [float(value)]
    return []


def check_record(
    record: Record, policy: Policy, checks: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Each check -> {check, ok, got}."""
    from record_engine.query import execute, parse

    results = []
    for c in checks:
        got: Any = None
        ok = False
        try:
            if c["type"] == "total":
                row = execute(parse(TOTAL), record, policy)["rows"][0]
                got = {
                    "sessions": row["count()"],
                    "days": row["count_distinct(date)"],
                    "minutes": _scenarios(row["sum(minutes)"]),
                }
                ok = (
                    ("sessions" not in c or got["sessions"] == c["sessions"])
                    and ("days" not in c or got["days"] == c["days"])
                    and ("minutes" not in c or got["minutes"] == sorted(map(float, c["minutes"])))
                )
            elif c["type"] == "week":
                rows = execute(parse(WEEKS), record, policy)["rows"]
                row = next(
                    (r for r in rows if str(r.get("group", "")).startswith(c["start"])), None
                )
                got = row["goal_met()"] if row else "no such week"
                ok = row is not None and row["goal_met()"]["status"] == c["status"]
            elif c["type"] == "fact":
                f = record.facts_of(c["subject"]).get(c["field"])
                got = (
                    None
                    if f is None
                    else {"value": f.value, "scenarios": f.scenarios, "status": f.status}
                )
                ok = f is not None
                if f is not None and ok and "value" in c:
                    ok = str(f.value) == str(c["value"]) or (
                        isinstance(f.value, (int, float)) and float(f.value) == float(c["value"])
                    )
                if f is not None and ok and "scenarios" in c:
                    ok = sorted(map(float, f.scenarios)) == sorted(map(float, c["scenarios"]))
                if f is not None and ok and "between" in c:
                    ok = (
                        f.value is not None and c["between"][0] <= float(f.value) <= c["between"][1]
                    )
                if f is not None and ok and "status" in c:
                    ok = f.status in c["status"]
            elif c["type"] == "no_event":
                got = [e.id for e in record.events if e.id == c["id"]]
                ok = not got
            elif c["type"] == "open_item":
                got = [o.text for o in record.open_items if o.kind == c["kind"]]
                ok = len(got) >= c.get("min", 1)
            elif c["type"] == "measurement":
                got = [
                    e.id
                    for e in record.events
                    if e.kind == "measurement"
                    and str(
                        done.value if (done := record.facts_of(e.id).get("completed_on")) else ""
                    )
                    == c["completed_on"]
                ]
                ok = bool(got)
        except Exception as error:  # a crash is a failed check, never a stopped run
            got = f"{type(error).__name__}: {error}"
            ok = False
        results.append({"check": c, "ok": ok, "got": got})
    return results


def answer_text(answer: dict[str, Any]) -> str:
    return " ".join(s.get("text", "") for s in (answer.get("answer") or {}).get("statements", []))


def check_answer(answer: dict[str, Any], question: dict[str, Any]) -> dict[str, Any]:
    text = answer_text(answer)
    published = answer.get("status") != "withheld"
    missing = [p for p in question.get("must", []) if not re.search(p, text, re.I)]
    forbidden = [p for p in question.get("must_not", []) if re.search(p, text, re.I)]
    return {
        "published": published,
        "missing": missing,
        "forbidden": forbidden,
        "ok": published and not missing and not forbidden,
    }


def cited_evidence(answer: dict[str, Any], record: Any, docs: list[Any]) -> list[dict[str, Any]]:
    """What the answer cites, resolved (source lines, facts, result rows), so the judge can check
    the citations instead of seeing IDs it cannot open."""
    from record_engine.evaluate import block_text

    lines_by_doc = {d.key: d.lines for d in docs}
    facts = {f.id: f for f in record.facts}
    rows = {row["id"]: row for r in answer.get("results", []) for row in r.get("rows", [])}
    statements = (answer.get("answer") or {}).get("statements", [])
    out = []
    for cite in sorted({c for s in statements for c in s.get("cites", [])}):
        if ":L" in cite:
            out.append({"id": cite, "quote": block_text(cite, lines_by_doc)})
        elif cite in facts:
            f = facts[cite]
            out.append(
                {
                    "id": cite,
                    "fact": f"{f.subject} {f.field} = {f.values()}",
                    "quotes": [e.quote for e in f.evidence][:2],
                }
            )
        elif cite in rows:
            out.append({"id": cite, "result_row": json.dumps(rows[cite], default=str)[:1500]})
    return out[:40]


def judge(
    question: dict[str, Any],
    answer: dict[str, Any],
    record: Any,
    docs: list[Any],
    added: list[str],
) -> dict[str, Any]:
    from record_engine.evaluate import JUDGE, SCHEMA

    if answer.get("status") == "withheld":
        return {"factual": 0, "evidence": 0, "missing_or_wrong": ["withheld"]}
    payload = {
        "question": question["question"],
        "reference_answer": question["reference"],
        # the scenario's changed documents, in full: the reference answer depends on them
        "documentary_evidence": [
            {"id": d.key, "excerpt": "\n".join(d.lines)[:6000]}
            for d in docs
            if any(d.key.startswith(Path(a).stem) for a in added)
        ],
        "candidates": [
            {
                "label": "candidate-1",
                "answer": {
                    "statements": [
                        {"text": s["text"], "kind": s["kind"]}
                        for s in (answer.get("answer") or {}).get("statements", [])
                    ]
                },
                "cited_evidence": cited_evidence(answer, record, docs),
            }
        ],
    }
    verdict = llm.call("scenario-grade", JUDGE, json.dumps(payload), SCHEMA, llm.WRITER, 3000)
    g = (verdict.get("answers") or [{}])[0]
    return {
        "factual": int(g.get("factual", 0)),
        "evidence": int(g.get("evidence", 0)),
        "missing_or_wrong": g.get("missing_or_wrong", []),
    }


def run_scenario(
    scenario: dict[str, Any], policy: Policy, documents: Path, root: Path, workers: int, grade: bool
) -> dict[str, Any]:
    from record_engine.evidence import PassageIndex
    from record_engine.qa import answer_question

    started = time.monotonic()
    folder = workspace(scenario, documents, root)
    with llm.scope() as usage:
        try:
            record, docs = build(folder, policy, root / scenario["id"], workers)
        except Exception as error:
            return {
                "id": scenario["id"],
                "title": scenario["title"],
                "error": f"build failed: {error}",
            }
        checks = check_record(record, policy, scenario.get("checks", []))
        index = PassageIndex(docs)
        answers = []
        for q in scenario.get("questions", []):
            a = answer_question(q["id"], q["question"], record, policy, index)
            result = {
                "id": q["id"],
                "question": q["question"],
                "status": a.get("status"),
                "answer": answer_text(a),
                "reasons": a.get("reasons", []),
                **check_answer(a, q),
            }
            if grade:
                result["judge"] = judge(q, a, record, docs, scenario.get("add", []))
            answers.append(result)
            (root / scenario["id"] / f"{q['id']}.json").write_text(
                json.dumps(a, indent=1, default=str)
            )
    return {
        "id": scenario["id"],
        "title": scenario["title"],
        "checks": checks,
        "answers": answers,
        "open_items_added": [
            o.text
            for o in record.open_items
            if o.kind in {"other_patient", "conflict", "candidate_link"}
        ][:8],
        "usage": {**usage.as_dict(), "seconds": round(time.monotonic() - started, 1)},
    }


def report_markdown(results: list[dict[str, Any]]) -> str:
    lines = ["# Scenario run", ""]
    n_checks = sum(len(r.get("checks", [])) for r in results)
    ok_checks = sum(c["ok"] for r in results for c in r.get("checks", []))
    answers = [a for r in results for a in r.get("answers", [])]
    lines += [
        f"Record checks passed: {ok_checks}/{n_checks}. "
        f"Answers published: {sum(a['published'] for a in answers)}/{len(answers)}; "
        f"answer checks passed: {sum(a['ok'] for a in answers)}/{len(answers)}"
        + (
            f"; judge factual {sum(a['judge']['factual'] for a in answers if 'judge' in a)}/{2 * sum('judge' in a for a in answers)}"
            if any("judge" in a for a in answers)
            else ""
        )
        + ".",
        "",
        "| Scenario | Record checks | Answers | Cost | Time |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        if "error" in r:
            lines.append(f"| {r['id']} {r['title']} | ERROR: {r['error']} | | | |")
            continue
        cs, ans = r["checks"], r["answers"]
        lines.append(
            f"| {r['id']} {r['title']} | {sum(c['ok'] for c in cs)}/{len(cs)} | "
            f"{sum(a['ok'] for a in ans)}/{len(ans)} | ${r['usage'].get('cost_usd', 0):.2f} | {r['usage']['seconds']} s |"
        )
    for r in results:
        if "error" in r:
            continue
        lines += ["", f"## {r['id']}: {r['title']}", ""]
        for c in r["checks"]:
            mark = "PASS" if c["ok"] else "FAIL"
            lines.append(
                f"- {mark} `{json.dumps(c['check'])}` → got `{json.dumps(c['got'], default=str)[:300]}`"
            )
        for a in r["answers"]:
            mark = "PASS" if a["ok"] else "FAIL"
            lines += [
                "",
                f"**{a['id']} ({mark}, {a['status']})** {a['question']}",
                "",
                f"> {a['answer'][:1500]}",
            ]
            if a["missing"] or a["forbidden"]:
                lines.append(f"- missing: {a['missing']}; forbidden present: {a['forbidden']}")
            if a["status"] == "withheld":
                lines.append(f"- withheld: {a['reasons'][:3]}")
            if "judge" in a:
                lines.append(
                    f"- judge: factual {a['judge']['factual']}, evidence {a['judge']['evidence']}; {a['judge']['missing_or_wrong'][:3]}"
                )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--documents", type=Path, default=Path("documents"))
    parser.add_argument("--out", type=Path, default=Path(".local/scenarios"))
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--judge", action="store_true")
    parser.add_argument("--policy", default=None)
    args = parser.parse_args()
    policy = load(args.policy)
    scenarios = json.loads((HERE / "scenarios.json").read_text())
    if args.only:
        scenarios = [s for s in scenarios if s["id"] in args.only]
    results = [
        run_scenario(s, policy, args.documents, args.out, args.workers, args.judge)
        for s in scenarios
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "report.json").write_text(json.dumps(results, indent=1, default=str))
    (args.out / "report.md").write_text(report_markdown(results))
    print(report_markdown(results).split("\n## ")[0])


if __name__ == "__main__":
    main()
