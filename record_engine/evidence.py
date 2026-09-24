"""Source-passage search and absence verification.

The structured record answers what it models; the source text is the ground truth for everything
else. Every question gets the passages that best match it (lexical BM25 over citable blocks), so a
narrative fact the queries did not reach can still be found and cited. And a claim that something
is *not documented* is checked against the source passages that best match it before it is
published: an absence claim is the easiest error to make and the hardest for a reader to notice.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from typing import Any

from record_engine import llm
from record_engine.ingest import Document

WORD = re.compile(r"[a-z0-9]+")
STOP = set(
    "a an and are as at be been by can did do does for from had has have how if in into is it its "
    "of on or that the their them they this those to was were what when where which who whom why "
    "with would should could each any all not no yes than then there these record records "
    "document documented documents documentation patient".split()
)


def terms(text: str) -> list[str]:
    return [t for t in WORD.findall(text.lower()) if t not in STOP and len(t) > 1]


class PassageIndex:
    """BM25 over every citable block of every document."""

    def __init__(self, documents: list[Document]):
        self.blocks: list[tuple[str, str, str]] = [
            (b.id, d.filename, b.text) for d in documents for b in d.blocks
        ]
        self.tokens = [terms(text) for _, _, text in self.blocks]
        self.df: Counter[str] = Counter(t for toks in self.tokens for t in set(toks))
        self.avg = sum(len(t) for t in self.tokens) / max(1, len(self.tokens))
        self.by_id = {bid: (name, text) for bid, name, text in self.blocks}

    def search(self, query: str, k: int = 8) -> list[dict[str, str]]:
        q = set(terms(query))
        n = len(self.blocks)
        scored = []
        for i, toks in enumerate(self.tokens):
            counts = Counter(toks)
            hits = [t for t in q if counts[t]]
            if not hits:
                continue
            score = 0.0
            for t in hits:
                idf = math.log(1 + (n - self.df[t] + 0.5) / (self.df[t] + 0.5))
                tf = counts[t]
                score += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * len(toks) / self.avg))
            scored.append((score, i))
        scored.sort(reverse=True)
        return [
            {"id": self.blocks[i][0], "file": self.blocks[i][1], "text": self.blocks[i][2][:700]}
            for _, i in scored[:k]
        ]

    def text(self, block_id: str) -> str | None:
        found = self.by_id.get(block_id)
        return found[1] if found else None


ABSENCE = """Each claim says something is NOT documented (or a part of a question was not answered
because the record lacks it). You get the passages from the source documents that best match
each claim. For each claim decide: does any passage document the thing the claim says is missing?
Only answer yes when a passage actually states it (a name, reason, time, value, event); a passage
that is merely on the same topic is not enough. A passage that says the thing did not happen, was
not done or is not included confirms the claim: answer no. Quote the words that state it."""

ABSENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer"},
                    "documented": {"type": "boolean"},
                    "passage": {"type": "string"},
                    "quote": {"type": "string"},
                },
                "required": ["index", "documented"],
            },
        }
    },
    "required": ["claims"],
}


def verify_absence(
    claims: list[str], question: str, index: PassageIndex, k: int = 5
) -> list[dict[str, Any]]:
    """For each absence claim: whether the source documents it after all, with the passage."""
    if not claims:
        return []
    items = []
    for n, claim in enumerate(claims):
        passages = index.search(f"{claim} {question}", k=k)
        items.append({"index": n, "claim": claim, "passages": passages})
    verdict = llm.call(
        "absence", ABSENCE, json.dumps({"claims": items}), ABSENCE_SCHEMA, llm.SMALL, 6000
    )
    out = []
    by_index = {v.get("index"): v for v in verdict.get("claims", []) if isinstance(v, dict)}
    for item in items:
        v = by_index.get(item["index"], {})
        passage = str(v.get("passage") or "")
        known = {str(p["id"]) for p in item["passages"]}  # type: ignore[attr-defined]
        out.append(
            {
                "claim": item["claim"],
                "documented": bool(v.get("documented")) and passage in known,
                "passage": passage if passage in known else None,
                "quote": v.get("quote"),
                "searched": [str(p["id"]) for p in item["passages"]],  # type: ignore[attr-defined]
            }
        )
    return out
