"""Grade the engine's held-out answers with the development benchmark's judge.

The reference answers (reference.json) enter only this grader, never the engine. The held-out
questions were written from the documents and are reported separately from the development
benchmark. Scores are advisory and unadjudicated.

    python -m record_engine.heldout.grade --answers .local/re_heldout/answers.json
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from record_engine.evaluate import answer_evidence, block_text, judge, summarize
from record_engine.ingest import ingest_folder
from record_engine.model import Record
from record_engine.render import block_texts

HERE = Path(__file__).parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", type=Path, default=Path(".local/re_heldout/answers.json"))
    parser.add_argument("--record", type=Path, default=None)
    parser.add_argument("--documents", type=Path, default=Path("documents"))
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    answers = {a["id"]: a for a in json.loads(args.answers.read_text())}
    questions = {q["id"]: q for q in json.loads((HERE / "questions.json").read_text())}
    references = {r["id"]: r for r in json.loads((HERE / "reference.json").read_text())}
    record = Record.model_validate_json(
        (args.record or args.answers.parent / "abstraction.json").read_text()
    )
    documents = ingest_folder(args.documents)
    lines_by_doc = {d.key: d.lines for d in documents}
    texts = block_texts(documents)

    def one(qid: str) -> dict[str, Any]:
        a = answers.get(qid) or {"status": "withheld"}
        if a.get("status") == "withheld":
            return {
                "id": qid,
                "status": "withheld",
                "factual": 0,
                "evidence": 0,
                "missing_or_wrong": ["No answer published"],
            }
        ref = references[qid]
        reference = {
            "reference_answer": ref["reference_answer"],
            "documentary_evidence": [
                {"id": s, "excerpt": block_text(s, lines_by_doc)} for s in ref["sources"]
            ],
        }
        verdict = judge(
            questions[qid]["question"],
            reference,
            a,
            # the same evidence the development judge sees: the source lines behind every
            # statement, including the records behind each cited query row
            answer_evidence(a, record, texts, lines_by_doc),
            "heldout-grade",
        )
        return {"id": qid, "status": a.get("status"), **verdict}

    with ThreadPoolExecutor(4) as pool:
        grades = list(pool.map(one, sorted(questions)))
    summary = summarize(
        grades, "model-assisted-unadjudicated, one candidate, author-written references"
    )
    out = args.out or args.answers.parent / "heldout_grades.json"
    out.write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k != "grades"}))


if __name__ == "__main__":
    main()
