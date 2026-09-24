"""Framing: checked statements are selected and ordered to answer the question; code keeps every
asked part answered and keeps a conflict or gap about what the lead states. Fake model, no calls."""

from __future__ import annotations

import pytest

from record_engine import llm, qa

STATEMENTS = [
    {"text": "12 sessions on 11 days.", "kind": "value", "cites": ["R1.all"]},
    {
        "text": "585 or 595 minutes; one start time conflicts.",
        "kind": "conflict",
        "cites": ["R1.all", "F-1"],
    },
    {"text": "Week 3 met the goal.", "kind": "value", "cites": ["R2.3"]},
    {"text": "Sleep improved by the end of January.", "kind": "narrative", "cites": ["F-9"]},
]


@pytest.fixture
def model(monkeypatch):
    def answer_with(out):
        def fake(stage, system, user, schema, model=None, max_tokens=0):
            if isinstance(out, Exception):
                raise out
            return out

        monkeypatch.setattr(llm, "call", fake)

    return answer_with


def test_off_question_statements_are_held_back(model):
    model({"parts": [{"part": "sessions and days", "statements": [0]}], "lead": [0], "context": []})
    out = qa.framed("How many sessions and days?", {"status": "answered", "statements": STATEMENTS})
    # the conflict shares the cited total with the lead, so it stays; goals and sleep do not
    assert [s["text"] for s in out["statements"]] == [STATEMENTS[0]["text"], STATEMENTS[1]["text"]]
    assert [s["text"] for s in out["omitted"]] == [STATEMENTS[2]["text"], STATEMENTS[3]["text"]]


def test_every_asked_part_keeps_an_answer(model):
    model(
        {
            "parts": [
                {"part": "sessions", "statements": [0]},
                {"part": "was the goal met", "statements": [2]},
            ],
            "lead": [0],
            "context": [],
        }
    )
    out = qa.framed("Sessions, and was the goal met?", {"statements": STATEMENTS})
    assert STATEMENTS[2] in out["statements"] and STATEMENTS[3] in out["omitted"]


def test_a_failed_or_empty_framing_keeps_every_statement(model):
    model(llm.ModelError("down"))
    assert qa.framed("Q?", {"statements": STATEMENTS})["statements"] == STATEMENTS
    model({"parts": [], "lead": [], "context": []})
    assert qa.framed("Q?", {"statements": STATEMENTS})["omitted"] == []


def test_framing_never_rewrites_a_statement(model):
    model({"parts": [], "lead": [3, 99, 3], "context": [0]})
    out = qa.framed("Q?", {"statements": STATEMENTS})
    assert out["statements"] == [STATEMENTS[3], STATEMENTS[0], STATEMENTS[1]]
