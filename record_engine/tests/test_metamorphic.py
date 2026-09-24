"""Document-level metamorphic tests on the real development record (offline; no model calls).

Each test changes the stored observations or documents the way a real record could differ and
checks that the record changes exactly as it should: a missing signature time cannot settle a
conflict, durations are never combined across documents, break disagreements stay scenarios,
partial weeks are not judged, copies add nothing and removing a correction restores the original.
"""

from __future__ import annotations

from pathlib import Path

from record_engine.ingest import ingest_folder, ingest_text
from record_engine.model import Grounded, Observation, Record, Relation
from record_engine.pipeline import read_observations
from record_engine.policy import load
from record_engine.query import execute, parse
from record_engine.reconcile import build_record

ROOT = Path(__file__).resolve().parents[2]
POLICY = load()
DOCUMENTS = ingest_folder(ROOT / "documents")
# a frozen extraction of documents/, so these tests need no model calls
OBSERVATIONS = read_observations(Path(__file__).parent / "observations.jsonl")
D110 = "BH-D110_individual_primary_record_2026-01-26"
D111 = "BH-D111_individual_second_record_2026-01-26"


def build(observations: list[Observation], documents=DOCUMENTS) -> Record:
    return build_record(documents, observations, POLICY)


def minutes(record: Record, event: str) -> list[float]:
    fact = record.facts_of(event)["minutes"]
    return sorted(fact.values())


def copy(observations: list[Observation]) -> list[Observation]:
    return [o.model_copy(deep=True) for o in observations]


def test_baseline_ledger():
    record = build(OBSERVATIONS)
    total = execute(
        parse(
            "from encounters where date >= 2026-01-05 and date <= 2026-01-30 and disposition = included select count(), count_distinct(date), sum(minutes)"
        ),
        record,
        POLICY,
    )["rows"][0]
    assert (total["count()"], total["count_distinct(date)"]) == (12, 11)
    assert total["sum(minutes)"] == {"scenarios": [585.0, 595.0]}
    assert minutes(record, "HG-E115") == [40.0, 50.0]
    assert minutes(record, "HG-E110") == [60.0]


def test_missing_signature_time_cannot_settle_a_conflict():
    changed = copy(OBSERVATIONS)
    for o in changed:
        if o.doc == D111:
            o.recorded = []
    record = build(changed)
    fact = record.facts_of("HG-E115")["minutes"]
    assert fact.status == "conflicting" and minutes(record, "HG-E115") == [40.0, 50.0]


def test_scenarios_are_never_combined_across_documents():
    changed = copy(OBSERVATIONS)
    for o in changed:
        if o.doc == D111:
            for f in o.fields:
                if f.name == "end" and f.value == "09:50":
                    f.value = "09:40"
                if f.name == "stated_minutes" and f.value == "40":
                    f.value = "30"
    record = build(changed)
    # D110 says 09:00–09:50 (50), D111 now 09:10–09:40 (30); 40 appears in no document
    assert minutes(record, "HG-E115") == [30.0, 50.0]


def test_disagreeing_breaks_are_scenarios_not_both_subtracted():
    extra = Observation(
        id="O-extra-break",
        doc="second_break_note",
        kind="interval",
        fields=[
            Grounded(
                name="encounter_id", value="HG-E102", quote="HG-E102", block="second_break_note:L1"
            ),
            Grounded(name="role", value="break", quote="break", block="second_break_note:L1"),
            Grounded(name="start", value="10:40", quote="10:40", block="second_break_note:L1"),
            Grounded(name="end", value="11:00", quote="11:00", block="second_break_note:L1"),
        ],
        evidence_kind="actual",
        attestation="signed",
    )
    documents = DOCUMENTS + [ingest_text("second_break_note.txt", "HG-E102 break 10:40–11:00")]
    record = build(copy(OBSERVATIONS) + [extra], documents)
    # presence 10:15–11:15: one note says break 10:45–11:00 (45), the other 10:40–11:00 (40)
    assert minutes(record, "HG-E102") == [40.0, 45.0]


def test_partial_week_is_not_judged_not_met():
    record = build(OBSERVATIONS)
    rows = execute(
        parse(
            "from encounters where date >= 2026-01-05 and date <= 2026-01-07 group_by week select goal_met()"
        ),
        record,
        POLICY,
    )["rows"]
    assert rows[0]["goal_met()"]["status"] == "cannot_determine"


def test_goal_applies_its_own_services_whatever_the_query_filter():
    record = build(OBSERVATIONS)
    week = "date >= 2026-01-19 and date <= 2026-01-25 group_by week select goal_met()"
    with_filter = execute(
        parse(f"from encounters where disposition = included and {week}"), record, POLICY
    )
    without = execute(parse(f"from encounters where {week}"), record, POLICY)
    assert (
        with_filter["rows"][0]["goal_met()"]["status"]
        == without["rows"][0]["goal_met()"]["status"]
        == "met"
    )


def test_an_exact_copy_of_a_document_adds_nothing():
    source = next(d for d in DOCUMENTS if d.key == "family_primary_jan09")
    duplicate = ingest_text("family_primary_jan09_resent.txt", "\n".join(source.lines))
    dup_obs = []
    for o in OBSERVATIONS:
        if o.doc == source.key:
            c = o.model_copy(deep=True)
            c.id = c.id + "-dup"
            c.doc = duplicate.key
            for f in c.fields:
                f.block = f.block.replace(source.key, duplicate.key)
            dup_obs.append(c)
    record = build(copy(OBSERVATIONS) + dup_obs, DOCUMENTS + [duplicate])
    assert record.copies.get(duplicate.key) == source.key
    assert minutes(record, "HG-E104") == [45.0]
    total = execute(
        parse("from encounters where disposition = included select count()"), record, POLICY
    )
    assert total["rows"][0]["count()"] == 12


def test_removing_the_correction_restores_the_original_departure():
    changed = [o for o in copy(OBSERVATIONS) if not o.doc.startswith("BH-D103")]
    documents = [d for d in DOCUMENTS if not d.key.startswith("BH-D103")]
    record = build(changed, documents)
    assert record.facts_of("HG-E110")["presence_end"].value == "11:30"
    assert minutes(record, "HG-E110") == [75.0]


def test_a_copy_falls_with_its_superseded_original():
    record = build(OBSERVATIONS)
    end = record.facts_of("HG-E110")["presence_end"]
    stances = {e.block.split(":")[0]: e.stance for e in end.evidence if e.value == "11:30"}
    assert stances.get("BH-D102_original_attendance_2026-01-19") == "superseded"
    assert all(s in {"superseded", "copy"} for s in stances.values())


def test_relation_type_is_required_for_supersession():
    # the same later value without a 'corrects' relation is a conflict, not a correction
    changed = copy(OBSERVATIONS)
    for o in changed:
        if o.doc.startswith("BH-D103"):
            o.relation = Relation()
    record = build(changed)
    assert record.facts_of("HG-E110")["presence_end"].status == "conflicting"
