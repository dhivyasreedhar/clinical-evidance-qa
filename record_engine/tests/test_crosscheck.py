"""The extraction cross-check: two readings compared by code, disagreements settled by a focused
re-read (two of three) or left open. The readings and the re-read are fakes; no model calls."""

from __future__ import annotations

import pytest

from record_engine import crosscheck
from record_engine.query import execute, parse
from record_engine.tests.test_engine import POLICY, docs, goal, visit

DOCS = docs("a", "b", "plan")


def readings(a, b, reread):
    """Patch the two readings (by trial) and the re-read (per document)."""
    calls = []

    def fake_observe_all(documents, policy, workers=6):
        from record_engine.llm import _SAMPLING

        trial = _SAMPLING.get()[1]
        return [o.model_copy(deep=True) for o in (b if trial else a)], [], []

    def fake_reread(document, policy, points, quotes):
        calls.append((document.key, sorted(p.field for p in points)))
        return [o.model_copy(deep=True) for o in reread.get(document.key, [])]

    return fake_observe_all, fake_reread, calls


@pytest.fixture
def patch(monkeypatch):
    def apply(a, b, reread):
        observe, fake_reread, calls = readings(a, b, reread)
        monkeypatch.setattr(crosscheck, "observe_all", observe)
        monkeypatch.setattr(crosscheck, "reread", fake_reread)
        return calls

    return apply


def minutes(record):
    rows = execute(parse("from encounters select sum(minutes)"), record, POLICY)["rows"]
    return rows[0]["sum(minutes)"]


def build(observations, problems):
    from record_engine.reconcile import build_record

    return build_record(DOCS, observations, POLICY, problems)


def test_agreeing_readings_need_no_reread(patch):
    both = goal() + [visit("A", "a", "V1", "2026-03-03", "09:00", "09:45")]
    calls = patch(both, both, {})
    observations, problems, report = crosscheck.observe_checked(DOCS, POLICY)
    assert report["disagreements"] == 0 and calls == []
    assert not [p for p in problems if p.kind == "reading_disagreement"]


def test_a_disputed_time_is_settled_by_the_reread_and_the_record_rebuilt(patch):
    # reading A took the session start for the patient's arrival; reading B and the re-read agree
    a = goal() + [visit("A", "a", "V1", "2026-03-03", "09:00", "09:45")]
    b = goal() + [visit("A", "a", "V1", "2026-03-03", "09:15", "09:45")]
    calls = patch(a, b, {"a": [visit("R", "a", "V1", "2026-03-03", "09:15", "09:45")]})
    observations, problems, report = crosscheck.observe_checked(DOCS, POLICY)
    assert calls == [("a", ["contact.start"])]
    assert report["settled"] == 1 and report["open"] == 0
    assert minutes(build(observations, problems)) == 30


def test_a_reread_that_agrees_with_neither_reading_leaves_the_point_open(patch):
    a = goal() + [visit("A", "a", "V1", "2026-03-03", "09:00", "09:45")]
    b = goal() + [visit("A", "a", "V1", "2026-03-03", "09:15", "09:45")]
    patch(a, b, {"a": [visit("R", "a", "V1", "2026-03-03", "09:05", "09:45")]})
    _observations, problems, report = crosscheck.observe_checked(DOCS, POLICY)
    assert report["open"] == 1
    [item] = [p for p in problems if p.kind == "reading_disagreement"]
    assert item.subject == "V1" and "09:00" in item.text and "09:15" in item.text


def test_a_department_named_as_issuer_is_not_a_disagreement(patch):
    # the same visit number read with the organisation, or with its appointment desk, is one issuer
    a = goal() + [
        visit("A", "a", "V1", "2026-03-03", "09:00", "09:45"),
        visit("D", "b", "V1", "2026-03-03", "09:00", "09:45"),
    ]
    b = [o.model_copy(deep=True) for o in a]
    from record_engine.model import Grounded

    b[-1].fields.append(Grounded(name="issuer", value="Riverside | Desk", quote="x", block="b:L1"))
    a[-1].fields.append(Grounded(name="issuer", value="Riverside", quote="x", block="b:L1"))
    calls = patch(a, b, {})
    _observations, _problems, report = crosscheck.observe_checked(DOCS, POLICY)
    assert report["disagreements"] == 0 and calls == []


def test_a_contact_one_reading_dated_and_the_other_did_not_is_paired_and_reread(patch):
    a = goal() + [visit("A", "a", "V1", "2026-03-03", "09:00", "09:45")]
    b = goal() + [visit("A", "a", "V2", "2026-03-03", "09:00", "09:45")]
    calls = patch(a, b, {"a": [visit("R", "a", "V1", "2026-03-03", "09:00", "09:45")]})
    observations, problems, report = crosscheck.observe_checked(DOCS, POLICY)
    assert calls and calls[0][0] == "a"
    assert report["open"] == 0
    record = build(observations, problems)
    assert [e.id for e in record.events if e.kind == "encounter"] == ["V1"]


def test_a_reread_that_invents_a_value_neither_reading_had_is_rejected(patch):
    a = goal() + [visit("A", "a", "V1", "2026-03-03", "09:00", "09:45")]
    b = goal() + [visit("A", "a", "V1", "2026-03-03", "09:15", "09:45")]
    # the re-read settles the start but also changes the end, which both readings agreed on
    invented = visit("R", "a", "V1", "2026-03-03", "09:15", "10:30")
    patch(a, b, {"a": [invented]})
    observations, problems, report = crosscheck.observe_checked(DOCS, POLICY)
    assert report["rereads_rejected"][0]["doc"] == "a"
    assert report["open"] == 1 and report["settled"] == 0
    assert {o.id for o in observations} == {o.id for o in a}
    assert [p.subject for p in problems if p.kind == "reading_disagreement"] == ["V1"]


def test_a_reread_may_add_what_both_readings_left_out(patch):
    from record_engine.model import Grounded

    a = goal() + [visit("A", "a", "V1", "2026-03-03", "09:00", "09:45")]
    b = goal() + [visit("A", "a", "V1", "2026-03-03", "09:15", "09:45")]
    reread_obs = visit("R", "a", "V1", "2026-03-03", "09:15", "09:45")
    # a stated duration neither reading extracted, in the disputed contact itself
    reread_obs.fields.append(Grounded(name="stated_minutes", value="30", quote="30", block="a:L1"))
    patch(a, b, {"a": [reread_obs]})
    observations, problems, report = crosscheck.observe_checked(DOCS, POLICY)
    assert report["rereads_rejected"] == [] and report["settled"] == 1
    assert build(observations, problems).facts_of("V1")["stated_minutes"].value == 30


def test_a_reread_replaces_only_the_disputed_kinds(patch):
    from record_engine.tests.test_engine import obs

    brk = obs(
        "B1",
        "a",
        "interval",
        [
            ("encounter_id", "V1", "V1"),
            ("role", "break", "break"),
            ("start", "09:30", "09:30"),
            ("end", "09:35", "09:35"),
        ],
    )
    a = goal() + [visit("A", "a", "V1", "2026-03-03", "09:00", "09:45"), brk]
    b = goal() + [visit("A", "a", "V1", "2026-03-03", "09:15", "09:45"), brk]
    # the re-read settles the contact's start but leaves out the undisputed break
    patch(a, b, {"a": [visit("R", "a", "V1", "2026-03-03", "09:15", "09:45")]})
    observations, problems, report = crosscheck.observe_checked(DOCS, POLICY)
    assert report["rereads_rejected"] == [] and report["settled"] == 1
    assert minutes(build(observations, problems)) == 25


def test_an_empty_reread_cannot_drop_a_visit_both_readings_have(patch):
    a = goal() + [visit("A", "a", "V1", "2026-03-03", "09:00", "09:45")]
    b = goal() + [visit("A", "a", "V1", "2026-03-03", "09:15", "09:45")]
    patch(a, b, {"a": []})
    observations, problems, report = crosscheck.observe_checked(DOCS, POLICY)
    assert report["rereads_rejected"][0]["doc"] == "a"
    record = build(observations, problems)
    assert [e.id for e in record.events if e.kind == "encounter"] == ["V1"]
    [item] = [p for p in problems if p.kind == "reading_disagreement"]
    assert item.text.endswith("the record uses the first reading.")


def test_a_reread_may_add_a_visit_both_readings_missed(patch):
    both = goal() + [visit("A", "a", "V1", "2026-03-03", "09:00", "09:45")]
    b = goal() + [visit("A", "a", "V1", "2026-03-03", "09:15", "09:45")]
    reread = [
        visit("R", "a", "V1", "2026-03-03", "09:15", "09:45"),
        visit("S", "a", "V5", "2026-03-04", "10:00", "10:30"),
    ]
    patch(both, b, {"a": reread})
    _observations, _problems, report = crosscheck.observe_checked(DOCS, POLICY)
    assert report["rereads_rejected"] == [] and report["settled"] == 1
