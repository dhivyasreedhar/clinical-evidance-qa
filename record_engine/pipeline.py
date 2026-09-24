"""Stage drivers: documents → observations (extract, validate, recall sweep), and JSONL I/O."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from record_engine import extract as ex
from record_engine import llm
from record_engine.ingest import Document
from record_engine.model import Observation, OpenItem
from record_engine.policy import Policy
from record_engine.validate import uncovered, validate


def observe(
    document: Document, policy: Policy
) -> tuple[list[Observation], list[OpenItem], dict[str, Any]]:
    """Extract, validate, sweep once, validate again. Returns observations, open items, stats."""
    first = ex.extract(document, policy)
    observations, problems = validate(document, ex.to_raw(document, first, "extract"), policy)
    missing = uncovered(document, observations)
    stats: dict[str, Any] = {
        "document": document.key,
        "observations_first_pass": len(observations),
        "mentions_uncovered_first_pass": len(missing),
        "dismissed": [],
    }
    dismissed: set[tuple[str, str]] = set()
    if missing:
        second = ex.re_extract(document, policy, missing)
        more, more_problems = validate(document, ex.to_raw(document, second, "sweep"), policy)
        observations += more
        problems += more_problems
        prefix = f"{document.key}:"
        for d in llm.as_list(second.get("dismissed"), ("mention", "block")):
            block = prefix + str(d.get("block", "")).strip("[] ")
            dismissed.add((block, d.get("mention", "")))
            stats["dismissed"].append(
                {"block": block, "mention": d.get("mention"), "reason": d.get("reason")}
            )
    remaining = uncovered(document, observations, dismissed)
    problems += [
        OpenItem(
            kind="unextracted_mention",
            subject=document.key,
            text=f"{kind} {text!r} is not covered by any observation",
            blocks=[block],
        )
        for block, kind, text in remaining
    ]
    stats["observations"] = len(observations)
    stats["mentions_uncovered_final"] = len(remaining)
    return observations, problems, stats


def observe_all(
    documents: list[Document], policy: Policy, workers: int = 6
) -> tuple[list[Observation], list[OpenItem], list[dict[str, Any]]]:
    with ThreadPoolExecutor(workers) as pool:
        results = list(pool.map(llm.carry(lambda d: observe(d, policy)), documents))
    observations = [o for r in results for o in r[0]]
    problems = [p for r in results for p in r[1]]
    stats = [r[2] for r in results]
    return observations, problems, stats


def write_jsonl(path: Path, rows: list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(r.model_dump(mode="json") if hasattr(r, "model_dump") else r) + "\n"
            for r in rows
        )
    )


def read_observations(path: Path) -> list[Observation]:
    return [Observation.model_validate_json(line) for line in path.read_text().splitlines() if line]
