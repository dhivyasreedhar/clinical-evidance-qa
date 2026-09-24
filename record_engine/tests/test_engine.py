"""Offline tests: no model calls. A synthetic second patient in a different domain (outpatient
physical therapy, Tuesday-start weeks, different instrument and ID formats) exercises the same
code the development record uses."""

from __future__ import annotations

from record_engine.ingest import ingest_text
from record_engine.model import Grounded, Observation, Recorded, Relation
from record_engine.policy import load
from record_engine.qa import code_check
from record_engine.query import QueryError, execute, parse
from record_engine.reconcile import build_record, creditable_minutes
from record_engine.validate import uncovered, validate

POLICY = load()

NOTE = """Riverside Physio | Physical therapy note
Visit V1 | March 3, 2026
Patient present 09:00–09:45. Stated treatment time: 45 minutes.

Signed: A. Lee, PT | March 3, 2026, 12:00"""


def g(name, value, doc, quote, line="L1"):
    return Grounded(name=name, value=value, quote=quote, block=f"{doc}:{line}")


def obs(
    oid, doc, kind, fields, evidence="actual", attestation="signed", recorded=None, relation=None
):
    return Observation(
        id=oid,
        doc=doc,
        kind=kind,
        fields=[g(n, v, doc, q) for n, v, q in fields],
        evidence_kind=evidence,
        attestation=attestation,
        recorded=[
            Recorded(role="signed", value=r, quote=r, block=f"{doc}:L1") for r in (recorded or [])
        ],
        relation=relation or Relation(),
    )


def docs(*keys):
    return [ingest_text(f"{k}.txt", "x") for k in keys]


# --- ingest and validation -------------------------------------------------------------------


def test_blocks_are_citable_line_ranges():
    d = ingest_text("pt_note.txt", NOTE)
    assert [b.id for b in d.blocks] == ["pt_note:L1-3", "pt_note:L5"]
    rows = ingest_text("t.txt", "a | b | c\n1 | 2 | 3\n4 | 5 | 6")
    assert [b.id for b in rows.blocks] == ["t:L1", "t:L2", "t:L3"]


def test_validation_requires_values_inside_their_quotes():
    d = ingest_text("pt_note.txt", NOTE)
    raw = [
        {
            "id": "O-1",
            "kind": "contact",
            "fields": [
                {
                    "name": "start",
                    "value": "09:00",
                    "quote": "Patient present 09:00–09:45",
                    "block": "pt_note:L1-3",
                },
                # derived by subtraction: 45 is stated, 44 is not
                {
                    "name": "stated_minutes",
                    "value": "44",
                    "quote": "09:00–09:45",
                    "block": "pt_note:L1-3",
                },
                {
                    "name": "date",
                    "value": "2026-03-03",
                    "quote": "March 3, 2026",
                    "block": "pt_note:L1-3",
                },
            ],
        }
    ]
    observations, problems = validate(d, raw, POLICY)
    assert {f.name for f in observations[0].fields} == {"start", "date"}
    assert any("duration_not_stated_in_quote" in p.text for p in problems)


def test_recall_sweep_lists_uncovered_mentions():
    d = ingest_text("pt_note.txt", NOTE)
    observations, _ = validate(
        d,
        [
            {
                "id": "O-1",
                "kind": "contact",
                "fields": [
                    {
                        "name": "encounter_id",
                        "value": "V1",
                        "quote": "Visit V1",
                        "block": "pt_note:L1-3",
                    }
                ],
            }
        ],
        POLICY,
    )
    kinds = {k for _, k, _ in uncovered(d, observations)}
    assert {"time", "duration", "date"} <= kinds


# --- reconciliation --------------------------------------------------------------------------


def goal(doc="plan"):
    return [
        obs(
            "G1",
            doc,
            "plan_goal",
            [
                ("threshold", "2", "2"),
                ("unit", "days", "days"),
                ("comparator", "at_least", "at least"),
                ("period", "week", "week"),
                ("week_start", "tuesday", "Tuesday"),
                ("eligible_services", "physical therapy", "physical therapy"),
            ],
        ),
        obs(
            "G2",
            doc,
            "plan_goal",
            [
                ("threshold", "80", "80"),
                ("unit", "minutes", "minutes"),
                ("comparator", "at_least", "at least"),
                ("period", "week", "week"),
                ("week_start", "tuesday", "Tuesday"),
                ("eligible_services", "physical therapy", "physical therapy"),
            ],
        ),
    ]


def visit(oid, doc, eid, day, start, end, **kw):
    fields = [
        ("encounter_id", eid, eid),
        ("date", day, day),
        ("service", "Physical therapy", "Physical therapy"),
        ("status_claim", "attended", "attended"),
        ("start", start, start),
        ("end", end, end),
    ]
    return obs(oid, doc, "contact", fields, **kw)


def test_correction_supersedes_only_its_field_and_copies_fall_with_the_original():
    observations = goal() + [
        visit("A", "note", "V1", "2026-03-03", "09:00", "09:45", recorded=["2026-03-03"]),
        visit(
            "B",
            "fix",
            "V1",
            "2026-03-03",
            "09:00",
            "09:40",
            recorded=["2026-03-06"],
            relation=Relation(type="corrects", fields=["end"], quote="q", block="fix:L1"),
        ),
        visit(
            "C",
            "resent",
            "V1",
            "2026-03-03",
            "09:00",
            "09:45",
            recorded=["2026-03-03"],
            relation=Relation(type="copy_of", quote="q", block="resent:L1"),
        ),
    ]
    record = build_record(docs("note", "fix", "resent", "plan"), observations, POLICY)
    facts = record.facts_of("V1")
    assert facts["presence_end"].value == "09:40" and facts["presence_end"].status == "established"
    assert {e.stance for e in facts["presence_end"].evidence if e.value == "09:45"} == {
        "superseded"
    }
    assert (
        facts["presence_start"].status == "corroborated"
    )  # note + correction; the copy adds nothing
    assert facts["minutes"].value == 40.0


def test_equal_sources_that_disagree_are_scenarios_and_signed_beats_draft():
    observations = goal() + [
        visit("A", "n1", "appt_778", "2026-03-10", "10:00", "10:30", recorded=["2026-03-10"]),
        visit("B", "n2", "appt_778", "2026-03-10", "10:00", "10:40", recorded=["2026-03-10"]),
        visit("C", "n3", "ENC-2026-0012", "2026-03-12", "08:00", "08:30", recorded=["2026-03-12"]),
        visit(
            "D",
            "n4",
            "ENC-2026-0012",
            "2026-03-12",
            "08:00",
            "09:00",
            attestation="draft",
            recorded=["2026-03-12"],
        ),
    ]
    record = build_record(docs("n1", "n2", "n3", "n4", "plan"), observations, POLICY)
    assert record.facts_of("appt_778")["minutes"].scenarios == [30.0, 40.0]
    assert any(o.kind == "conflict" and o.subject == "appt_778" for o in record.open_items)
    enc = record.facts_of("ENC-2026-0012")
    assert enc["presence_end"].value == "08:30" and enc["presence_end"].rule == "precedence"


def test_breaks_subtract_and_templates_or_charges_never_prove_attendance():
    observations = goal() + [
        visit("A", "roster", "12345", "2026-03-17", "13:00", "14:30"),
        obs(
            "B",
            "content",
            "interval",
            [
                ("encounter_id", "12345", "12345"),
                ("role", "break", "break"),
                ("start", "13:40", "13:40"),
                ("end", "13:55", "13:55"),
            ],
        ),
        obs(
            "C",
            "draft",
            "contact",
            [
                ("encounter_id", "777", "777"),
                ("date", "2026-03-18", "2026-03-18"),
                ("status_claim", "attended", "attended"),
                ("service", "Physical therapy", "Physical therapy"),
            ],
            evidence="templated",
            attestation="draft",
        ),
        obs(
            "D",
            "charge",
            "contact",
            [
                ("encounter_id", "777", "777"),
                ("date", "2026-03-18", "2026-03-18"),
                ("service", "Physical therapy", "Physical therapy"),
            ],
            evidence="billed",
        ),
    ]
    record = build_record(
        docs("roster", "content", "draft", "charge", "plan"), observations, POLICY
    )
    assert record.facts_of("12345")["minutes"].value == 75.0
    assert record.facts_of("777")["disposition"].value == "no_actual_record"


def test_interval_algebra_clips_breaks_to_presence():
    assert creditable_minutes("10:15", "11:15", [("10:45", "11:00"), ("09:00", "09:30")]) == 45.0


# --- query language --------------------------------------------------------------------------


def record_two_weeks():
    observations = goal() + [
        visit("A", "a", "V1", "2026-03-03", "09:00", "09:45"),  # Tuesday, week 1
        visit("B", "b", "V2", "2026-03-05", "09:00", "09:30"),
        visit("C1", "c1", "V3", "2026-03-10", "10:00", "10:30"),  # week 2, conflicting
        visit("C2", "c2", "V3", "2026-03-10", "10:00", "10:40"),
    ]
    return build_record(docs("a", "b", "c1", "c2", "plan"), observations, POLICY)


def test_weeks_start_on_the_goal_weekday_and_scenarios_carry_through():
    record = record_two_weeks()
    result = execute(
        parse(
            "from encounters where date >= 2026-03-03 and date <= 2026-03-16 and disposition = included group_by week select count_distinct(date), sum(minutes), goal_met()"
        ),
        record,
        POLICY,
    )
    weeks = {r["group"]: r for r in result["rows"]}
    assert set(weeks) == {"2026-03-03..2026-03-09", "2026-03-10..2026-03-16", "all groups"}
    overall = weeks.pop("all groups")  # totals across weeks, computed by code
    assert overall["count_distinct(date)"] == 3
    assert overall["sum(minutes)"] == {"scenarios": [105.0, 115.0]}
    assert "goal_met()" not in overall
    assert weeks["2026-03-03..2026-03-09"]["goal_met()"]["status"] == "not_met"  # 75 < 80
    second = weeks["2026-03-10..2026-03-16"]
    assert second["sum(minutes)"] == {"scenarios": [30.0, 40.0]}
    assert second["goal_met()"]["status"] == "not_met"  # one day < 2


def test_sum_never_adds_the_two_sides_of_a_conflict():
    record = record_two_weeks()
    result = execute(parse("from encounters select sum(minutes)"), record, POLICY)
    assert result["rows"][0]["sum(minutes)"] == {"scenarios": [105.0, 115.0]}


def test_bad_queries_raise_for_the_planner_retry():
    for text in (
        "select count()",
        "from nowhere",
        "from encounters where date >= tuesday",
        "from encounters select frobnicate()",
    ):
        try:
            execute(parse(text), record_two_weeks(), POLICY)
        except QueryError:
            continue
        raise AssertionError(text)


# --- answer checks ---------------------------------------------------------------------------


def test_binding_catches_numbers_not_in_cited_values_and_partial_conflicts():
    record = record_two_weeks()
    results = [execute(parse("from encounters select count(), sum(minutes)"), record, POLICY, "R1")]
    good = {
        "statements": [
            {"text": "3 visits, 105 or 115 minutes.", "kind": "conflict", "cites": ["R1.1"]}
        ]
    }
    assert code_check(good, results, record)[0] == []
    invented = {
        "statements": [{"text": "3 visits, 110 minutes.", "kind": "value", "cites": ["R1.1"]}]
    }
    assert any("110" in i for i in code_check(invented, results, record)[0])
    v3 = next(f for f in record.facts if f.subject == "V3" and f.field == "minutes")
    settled = {"statements": [{"text": "V3 lasted 40 minutes.", "kind": "value", "cites": [v3.id]}]}
    assert any("state every scenario" in i for i in code_check(settled, results, record)[0])


def test_or_and_parentheses_in_where():
    record = record_two_weeks()
    both = execute(
        parse(
            "from encounters where (id = V1 or id = V3) and disposition = included select count()"
        ),
        record,
        POLICY,
    )
    assert both["rows"][0]["count()"] == 2
    single = execute(parse("from encounters where (id = V2) select count()"), record, POLICY)
    assert single["rows"][0]["count()"] == 1


def test_explicit_patient_interval_beats_the_contact_session_span():
    note = [
        visit("C", "fam", "F1", "2026-03-19", "13:00", "13:45"),  # whole session on the contact
        obs(
            "I",
            "fam",
            "interval",
            [
                ("encounter_id", "F1", "F1"),
                ("role", "presence", "presence"),
                ("patient_present", "yes", "present"),
                ("start", "13:15", "13:15"),
                ("end", "13:45", "13:45"),
            ],
        ),
    ]
    record = build_record(docs("fam", "plan"), goal() + note, POLICY)
    assert record.facts_of("F1")["minutes"].value == 30.0
    assert record.facts_of("F1")["session_minutes"].value == 45.0


def test_a_call_about_a_missed_visit_stays_its_own_contact():
    missed = obs(
        "M",
        "log",
        "contact",
        [
            ("encounter_id", "V9", "V9"),
            ("date", "2026-03-20", "2026-03-20"),
            ("service", "Physical therapy", "Physical therapy"),
            ("status_claim", "no_show", "no show"),
        ],
    )
    call = obs(
        "K",
        "log",
        "contact",
        [
            ("date", "2026-03-20", "2026-03-20"),
            ("service", "outbound phone call", "outbound phone call"),
            ("mode", "phone call", "phone call"),
            ("start", "15:30", "15:30"),
            ("end", "15:35", "15:35"),
        ],
    )
    record = build_record(docs("log", "plan"), goal() + [missed, call], POLICY)
    encounters = [e for e in record.events if e.kind == "encounter"]
    assert len(encounters) == 2


def test_code_proves_citations_and_simple_arithmetic_but_not_invented_numbers():
    record = record_two_weeks()
    week1 = execute(
        parse(
            "from encounters where date >= 2026-03-03 and date <= 2026-03-09 and disposition = included select count()"
        ),
        record,
        POLICY,
        "R1",
    )
    week2 = execute(
        parse(
            "from encounters where date >= 2026-03-10 and date <= 2026-03-16 and disposition = included select count()"
        ),
        record,
        POLICY,
        "R2",
    )
    results = [week1, week2]
    # 2 then 1 visit: 3 in total is a verified sum of cited counts
    diff = {
        "statements": [
            {
                "text": "There were 3 visits across both weeks.",
                "kind": "value",
                "cites": ["R1.1", "R2.1"],
            }
        ]
    }
    issues, _ = code_check(diff, results, record)
    assert issues == []
    from record_engine.qa import _arithmetic

    assert _arithmetic(2.0, {7.0, 5.0}) == "7 − 5"
    assert _arithmetic(62.5, {5.0, 8.0}) == "5 / 8 × 100"
    assert _arithmetic(110.0, {105.0, 3.0}) is None
    invented = {
        "statements": [{"text": "Visits fell by 7.", "kind": "value", "cites": ["R1.1", "R2.1"]}]
    }
    assert code_check(invented, results, record)[0]


def test_narrative_dates_must_match_their_evidence():
    record = record_two_weeks()
    v1 = next(f for f in record.facts if f.subject == "V1" and f.field == "presence_start")
    moved = {
        "statements": [
            {
                "text": "On March 10 the patient arrived at 09:00.",
                "kind": "narrative",
                "cites": [v1.id],
            }
        ]
    }
    assert any("not a date of its cited evidence" in i for i in code_check(moved, [], record)[0])
    right = {
        "statements": [
            {
                "text": "On March 3 the patient arrived at 09:00.",
                "kind": "narrative",
                "cites": [v1.id],
            }
        ]
    }
    assert code_check(right, [], record)[0] == []


def test_passage_search_finds_the_block_that_states_it():
    from record_engine.evidence import PassageIndex

    documents = [
        ingest_text(
            "desk.txt",
            "Desk log\n\nJanuary 6: Alex was delayed finding parking.\n\nJanuary 22: arrived 10:30.",
        ),
        ingest_text("note.txt", "Group note\n\nCoping skills practised."),
    ]
    hits = PassageIndex(documents).search("why was the patient late parking", k=1)
    assert hits[0]["id"] == "desk:L3"


def test_a_plain_field_beside_an_aggregate_groups_by_it_and_text_dates_compare_as_dates():
    record = record_two_weeks()
    result = execute(parse("from encounters select date, count()"), record, POLICY)
    assert result["implicit_group_by"] == "date"
    counts = {r["group"]: r["count()"] for r in result["rows"]}
    assert counts == {"2026-03-03": 1, "2026-03-05": 1, "2026-03-10": 1, "all groups": 3}
    assert result["rows"][-1]["groups"] == 3  # distinct dates, computed by code
    goals = execute(parse("from goals where date >= 2026-01-01 select count()"), record, POLICY)
    assert goals["rows"]  # no crash when a source holds dates as text


def test_elapsed_time_question_numbers_and_serialized_statements():
    from record_engine.qa import _elapsed, normalize_answer

    assert _elapsed(10.0, {"13:20", "13:30"}) == "13:30 − 13:20"
    assert _elapsed(7.0, {"13:20", "13:30"}) is None
    record = record_two_weeks()
    v1 = next(f for f in record.facts if f.subject == "V1" and f.field == "presence_start")
    premise = {
        "statements": [
            {"text": "A 55-minute figure is not supported.", "kind": "value", "cites": [v1.id]}
        ]
    }
    assert code_check(premise, [], record)[0]
    assert code_check(premise, [], record, question="Is 55 minutes right?")[0] == []
    text = '[{"text": "It was held.", "kind": "narrative", "cites": ["F-1"]}]'
    assert normalize_answer({"statements": text})["statements"][0]["text"] == "It was held."
    cut = text[:-1] + ', {"text": "Cut off'  # a truncated list keeps its complete statements
    assert [s["text"] for s in normalize_answer({"statements": cut})["statements"]] == [
        "It was held."
    ]


def test_a_named_range_binds_by_its_endpoints():
    from datetime import date

    from record_engine.dates import find_dates

    assert len(find_dates("January 12\u201318, 2026")) == 7
    assert find_dates("January 12\u201318, 2026", expand=False) == {
        date(2026, 1, 12),
        date(2026, 1, 18),
    }


def test_absence_claims_are_found_inside_any_statement():
    from record_engine.qa import absence_sentences

    text = (
        "V1 lasted 45 minutes. The record does not document a duration for the collateral "
        "contact. The partner attended."
    )
    assert absence_sentences(text) == [
        "The record does not document a duration for the collateral contact."
    ]
    assert absence_sentences("Both notes were signed.") == []


# --- regression tests for generic answer and record checks (synthetic patient only) ----------


def caregiver_contact():
    """A caregiver-only contact on March 18: the patient absent, 14:00-14:40 documented."""
    return obs(
        "CG",
        "caregiver",
        "contact",
        [
            ("encounter_id", "V7", "V7"),
            ("date", "2026-03-18", "2026-03-18"),
            ("service", "caregiver collateral", "caregiver collateral"),
            ("status_claim", "not_present", "patient absent"),
            ("patient_present", "no", "absent"),
            ("start", "14:00", "14:00"),
            ("end", "14:40", "14:40"),
        ],
    )


def test_an_absence_claim_is_checked_against_the_facts_before_the_passages():
    from record_engine.qa import absence_in_facts

    record = build_record(docs("caregiver", "plan"), goal() + [caregiver_contact()], POLICY)
    hits = absence_in_facts(
        "The record does not document a duration for the March 18 collateral contact.",
        record,
        POLICY,
    )
    assert [(f.subject, f.field, f.value) for f in hits] == [("V7", "session_minutes", 40.0)]
    # the same claim about a date with nothing on it, or a relative claim, is not settled here
    assert absence_in_facts("No duration is documented for March 19.", record, POLICY) == []
    assert (
        absence_in_facts(
            "No duration is recorded between March 18 and March 25 for any caregiver contact.",
            record,
            POLICY,
        )
        == []
    )
    assert (
        absence_in_facts(
            "The record does not document a duration for any other contact after March 18.",
            record,
            POLICY,
        )
        == []
    )
    # a date in another clause is context, not the missing item
    assert (
        absence_in_facts(
            "The record does not document whether contact continued — the March 18 collateral "
            "contact's duration rests on one note.",
            record,
            POLICY,
        )
        == []
    )
    # the claim's own clause still settles it, after a lead-in
    assert absence_in_facts(
        "Duration: the record does not document a duration for the March 18 collateral contact.",
        record,
        POLICY,
    )


def booking(oid, doc, claim, quote):
    return obs(
        oid,
        doc,
        "contact",
        [
            ("encounter_id", "V8", "V8"),
            ("date", "2026-03-24", "2026-03-24"),
            ("service", "Physical therapy", "Physical therapy"),
            ("status_claim", claim, quote),
        ],
    )


def test_appointment_status_is_reconciled_and_attendance_follows_it():
    # a generic cancellation is refined by one naming who cancelled
    refined = build_record(
        docs("desk", "register", "plan"),
        goal()
        + [
            booking("D", "desk", "cancelled_unspecified", "cancelled"),
            booking("R", "register", "cancelled_by_patient", "patient cancelled"),
        ],
        POLICY,
    )
    status = refined.facts_of("V8")["status"]
    assert (status.value, status.rule) == ("cancelled_by_patient", "specific_refines_generic")
    assert refined.facts_of("V8")["attendance"].value == "not_attended"
    # a no-show and a patient cancellation from equal sources are a conflict, not a choice
    disputed = build_record(
        docs("desk", "register", "plan"),
        goal()
        + [
            booking("D", "desk", "no_show", "no show"),
            booking("R", "register", "cancelled_by_patient", "patient cancelled"),
        ],
        POLICY,
    )
    status = disputed.facts_of("V8")["status"]
    assert status.status == "conflicting"
    assert set(status.scenarios) == {"no_show", "cancelled_by_patient"}
    assert disputed.facts_of("V8")["attendance"].value == "not_attended"  # both mean not there
    rows = execute(parse("from encounters where id = V8 select rows()"), disputed, POLICY)
    assert "appointment_status" in rows["rows"][0]["rows()"][0]


def test_order_based_aggregates_never_split_the_set_by_a_plain_field():
    scores = [
        obs(
            f"S{n}",
            f"m{n}",
            "measurement",
            [
                ("instrument", "LEFS", "LEFS"),
                ("score", str(score), str(score)),
                ("completed_on", day, day),
            ],
        )
        for n, (score, day) in enumerate(
            [(40, "2026-03-03"), (52, "2026-03-17"), (61, "2026-03-31")]
        )
    ]
    record = build_record(docs("m0", "m1", "m2", "plan"), goal() + scores, POLICY)
    result = execute(parse("from measurements select date, score, change(score)"), record, POLICY)
    assert "implicit_group_by" not in result
    assert len(result["rows"]) == 1
    assert result["rows"][0]["change(score)"]["change"] == 21.0
    grouped = execute(parse("from measurements select date, count()"), record, POLICY)
    assert grouped["implicit_group_by"] == "date"  # counts still group


def test_date_binding_is_repaired_by_code_or_the_clause_is_dropped():
    from record_engine.evidence import PassageIndex
    from record_engine.qa import repair_dates

    index = PassageIndex(
        [
            ingest_text(
                "desk.txt", "Desk log\n\nMarch 10: patient phoned to say the bus was late."
            ),
            ingest_text("note.txt", "PT note\n\nMarch 3: gait training, 45 minutes."),
        ]
    )
    answer = {
        "statements": [
            {
                "text": "On March 10 the patient phoned to say the bus was late.",
                "kind": "narrative",
                "cites": ["note:L3"],
            },
            {
                "text": "Gait training was done. On March 12 the patient felt better.",
                "kind": "narrative",
                "cites": ["note:L3"],
            },
        ]
    }
    issues = [
        "statement 0: date 2026-03-10 is not a date of its cited evidence (2026-03-03); cite ...",
        "statement 1: date 2026-03-12 is not a date of its cited evidence (2026-03-03); cite ...",
    ]
    passages: dict[str, str] = {}
    done = repair_dates(answer, issues, passages, index)
    assert "desk:L3" in answer["statements"][0]["cites"] and "desk:L3" in passages
    assert answer["statements"][1]["text"] == "Gait training was done."
    assert len(done) == 2


def test_release_gate_ids_expand_and_fail_on_withheld(tmp_path):
    import json

    from record_engine.__main__ import expand_ids, gate_failures

    assert expand_ids(["DEV-01..03", "X-9"]) == ["DEV-01", "DEV-02", "DEV-03", "X-9"]
    answers = tmp_path / "answers.json"
    answers.write_text(
        json.dumps([{"id": "DEV-01", "status": "answered"}, {"id": "DEV-02", "status": "withheld"}])
    )
    assert gate_failures(answers, ["DEV-01", "DEV-02", "DEV-03"]) == ["DEV-02", "DEV-03"]


def test_a_checklist_total_must_be_stated_from_the_row_that_computes_it():
    record = record_two_weeks()
    result = execute(
        parse("from encounters where disposition = included group_by week select sum(minutes)"),
        record,
        POLICY,
    )
    need = [{"item": "combined minutes across both weeks", "query": 1}]
    per_week = {
        "statements": [
            {"text": "Week 1 had 75 minutes.", "kind": "value", "cites": [result["rows"][0]["id"]]}
        ]
    }
    issues, _ = code_check(per_week, [result], record, required_totals=need)
    assert any("needs the combined figure" in i and "R1.all" in i for i in issues)
    total = {
        "statements": [
            {"text": "In all, 105 or 115 minutes.", "kind": "value", "cites": ["R1.all"]}
        ]
    }
    issues, _ = code_check(total, [result], record, required_totals=need)
    assert not any("combined figure" in i for i in issues)
    # no checklist item marked as a total: nothing is required, whatever the wording
    issues, _ = code_check(per_week, [result], record, question="What was the total time?")
    assert not any("combined figure" in i for i in issues)


def test_every_date_the_question_names_must_be_inside_a_query_window():
    from record_engine.qa import window_errors

    record = record_two_weeks()
    narrow = {"queries": [{"query": "from encounters where date = 2026-03-03 select count()"}]}
    errors = window_errors("What happened on March 3 and March 10?", narrow, record)
    assert len(errors) == 1 and "2026-03-10" in errors[0]
    open_ended = {"queries": [{"query": "from encounters select count()"}]}
    assert window_errors("What happened on March 10?", open_ended, record) == []


def test_the_writer_gets_the_record_around_the_question_not_only_the_results():
    from record_engine.qa import record_context

    record = build_record(docs("caregiver", "plan"), goal() + [caregiver_contact()], POLICY)
    facts, _ = record_context([], record, "What happened on March 18?")
    fields = {(f["subject"], f["field"]) for f in facts}
    assert ("V7", "session_minutes") in fields and ("V7", "status") in fields


def test_a_correction_stated_on_the_document_applies_to_its_observations():
    original = visit("A", "roster", "V1", "2026-03-03", "09:00", "09:45", recorded=["2026-03-03"])
    meta = obs(
        "M",
        "fix",
        "doc_meta",
        [("title", "Attendance correction", "Attendance correction")],
        relation=Relation(
            type="corrects", fields=["end"], quote="departure is 09:30", block="fix:L1"
        ),
    )
    corrected = visit("C", "fix", "V1", "2026-03-03", "09:00", "09:30", recorded=["2026-03-04"])
    record = build_record(
        docs("roster", "fix", "plan"), goal() + [original, meta, corrected], POLICY
    )
    end = record.facts_of("V1")["presence_end"]
    assert (end.value, end.rule) == ("09:30", "signed_correction_supersedes_original")


def test_a_stated_duration_for_the_patient_segment_beats_the_session_duration():
    note = [
        obs(
            "C",
            "fam",
            "contact",
            [
                ("encounter_id", "F1", "F1"),
                ("date", "2026-03-19", "2026-03-19"),
                ("service", "Physical therapy", "Physical therapy"),
                ("status_claim", "attended", "attended"),
                ("stated_minutes", "45", "45 minutes"),
            ],
        ),
        obs(
            "I",
            "fam",
            "interval",
            [
                ("encounter_id", "F1", "F1"),
                ("role", "presence", "presence"),
                ("patient_present", "yes", "present"),
                ("start", "13:15", "13:15"),
                ("end", "13:45", "13:45"),
                ("stated_minutes", "30", "30 minutes"),
            ],
        ),
    ]
    record = build_record(docs("fam", "plan"), goal() + note, POLICY)
    assert record.facts_of("F1")["stated_minutes"].value == 30.0
    assert record.facts_of("F1")["minutes"].value == 30.0


def test_a_missing_comma_between_functions_is_read_through():
    q = parse("from measurements select list(date, score) change(score)")
    assert [a.name for a in q.select] == ["list", "change"]


def test_a_goal_outcome_must_match_the_computed_threshold_outcome():
    record = record_two_weeks()
    result = execute(
        parse(
            "from encounters where date >= 2026-03-03 and date <= 2026-03-16 and disposition = "
            "included group_by week select count_distinct(date), sum(minutes), goal_met()"
        ),
        record,
        POLICY,
    )
    first = result["rows"][0]  # week of March 3: 2 days (met), 75 minutes (not met)
    goal = first["goal_met()"]
    assert [b["outcome"] for b in goal["by_threshold"]] == ["met", "not_met"]
    assert goal["overall"] == "not_met"
    wrong = {
        "statements": [
            {
                "text": "In the week of March 3 both the days goal and the minutes goal were not met.",
                "kind": "value",
                "cites": [first["id"]],
            }
        ]
    }
    issues, _ = code_check(wrong, [result], record)
    assert any("days goal" in i and "computed result for that week is met" in i for i in issues)
    right = {
        "statements": [
            {
                "text": "In the week of March 3 the days goal was met but the minutes goal was not met.",
                "kind": "value",
                "cites": [first["id"]],
            }
        ]
    }
    issues, _ = code_check(right, [result], record)
    assert not any("goal for" in i for i in issues)


def test_a_missing_quantity_the_record_holds_is_re_planned():
    from record_engine.qa import computable_gaps

    record = build_record(docs("caregiver", "plan"), goal() + [caregiver_contact()], POLICY)
    gap = {
        "statements": [
            {
                "text": "The percent change in minutes is not documented.",
                "kind": "missing",
                "cites": [],
            }
        ]
    }
    assert computable_gaps(gap, record)
    other = {
        "statements": [
            {
                "text": "No reason for the change of therapist is given.",
                "kind": "missing",
                "cites": [],
            }
        ]
    }
    assert computable_gaps(other, record) == []


def test_header_fields_said_to_be_missing_are_looked_up_in_every_document():
    from record_engine.qa import absence_in_facts

    header = obs(
        "H",
        "caregiver",
        "doc_meta",
        [("title", "Caregiver note", "Caregiver note"), ("patient_mrn", "RP-778", "MRN RP-778")],
    )
    record = build_record(docs("caregiver", "plan"), goal() + [caregiver_contact(), header], POLICY)
    hits = absence_in_facts("The patient's MRN is not documented in these records.", record, POLICY)
    assert [(f.field, f.value) for f in hits] == [("patient_mrn", "RP-778")]


def test_weekdays_and_remaining_balances_are_checked_by_code():
    from datetime import date

    from record_engine.qa import weekday_issues

    first, last = date(2026, 3, 1), date(2026, 3, 31)
    assert weekday_issues(0, "Tuesday, March 3", first, last) == []
    issues = weekday_issues(0, "March 7 (Thursday)", first, last)
    assert len(issues) == 1 and "is a Saturday, not a Thursday" in issues[0]
    record = record_two_weeks()
    counts = execute(parse("from encounters select count()"), record, POLICY)
    balance = {
        "statements": [
            {
                "text": "Of 5 authorized visits, 2 remain.",
                "kind": "value",
                "cites": [counts["rows"][0]["id"]],
            }
        ]
    }
    counts["rows"][0]["authorized"] = 5.0  # a cited value the model subtracts from
    issues, _ = code_check(balance, [counts], record)
    assert any("remaining balance" in i for i in issues)


def test_rows_carry_weekday_delivered_and_their_documents():
    record = build_record(
        docs("desk", "register", "plan", "a"),
        goal()
        + [
            booking("D", "desk", "no_show", "no show"),
            visit("A", "a", "V1", "2026-03-03", "09:00", "09:45"),
        ],
        POLICY,
    )
    rows = {
        r["id"]: r
        for r in execute(parse("from encounters select rows()"), record, POLICY)["rows"][0][
            "rows()"
        ]
    }
    assert rows["V1"]["weekday"] == "Tuesday" and rows["V1"]["delivered"] == "yes"
    assert rows["V8"]["delivered"] == "no"
    assert rows["V1"]["documents"] == ["a"]


def test_answer_checks_do_not_misfire():
    from datetime import date

    from record_engine.qa import stated, weekday_issues

    first, last = date(2026, 3, 1), date(2026, 3, 31)
    # each weekday is read against its own date, and a year beside a date is not a value
    text = "The week runs March 2 (Monday) through March 8 (Sunday), 2026."
    assert weekday_issues(0, text, first, last) == []
    assert stated(text, [])[0] == set()
    # a list of week numbers is a list of labels, not values
    assert stated("The days goal was met in weeks 1, 3, and 4.", [])[0] == set()
    # a scenario's outcome is not the computed status
    record = record_two_weeks()
    result = execute(
        parse(
            "from encounters where date >= 2026-03-03 and date <= 2026-03-16 and disposition = "
            "included group_by week select sum(minutes), goal_met()"
        ),
        record,
        POLICY,
    )
    second = result["rows"][1]
    scenario = {
        "statements": [
            {
                "text": "For the week of March 10 the minutes goal: in the 30-minute scenario it is "
                "not met.",
                "kind": "conflict",
                "cites": [second["id"]],
            }
        ]
    }
    assert not any("goal for" in i for i in code_check(scenario, [result], record)[0])


def test_a_figure_no_query_computed_asks_the_planner_and_a_per_week_item_needs_no_total():
    from record_engine.qa import uncomputed_figures

    answer = {
        "statements": [
            {"text": "The score fell 28.6 percent from March 10.", "kind": "value", "cites": []}
        ]
    }
    issue = ["statement 0: 28.6 is in no cited result, fact or passage and is not a sum ..."]
    assert uncomputed_figures(answer, issue)
    record = record_two_weeks()
    result = execute(
        parse("from encounters where disposition = included group_by week select sum(minutes)"),
        record,
        POLICY,
    )
    per_week = {
        "statements": [
            {"text": "Week 1 had 75 minutes.", "kind": "value", "cites": [result["rows"][0]["id"]]}
        ]
    }
    listed = [{"item": "minutes for each week", "query": 1}]
    assert not any(
        "combined figure" in i
        for i in code_check(per_week, [result], record, required_totals=listed)[0]
    )


def test_a_corrected_account_gives_no_second_session_length():
    original = visit("A", "roster", "V1", "2026-03-03", "09:00", "09:45", recorded=["2026-03-03"])
    corrected = visit(
        "C",
        "fix",
        "V1",
        "2026-03-03",
        "09:00",
        "09:30",
        recorded=["2026-03-04"],
        relation=Relation(type="corrects", fields=["end"], quote="departure 09:30", block="fix:L1"),
    )
    record = build_record(docs("roster", "fix", "plan"), goal() + [original, corrected], POLICY)
    session = record.facts_of("V1")["session_minutes"]
    assert (session.value, session.status) == (30.0, "documented")


def test_goal_outcomes_are_read_per_threshold_and_scenarios_are_exempt():
    record = record_two_weeks()
    result = execute(
        parse(
            "from encounters where date >= 2026-03-03 and date <= 2026-03-16 and disposition = "
            "included group_by week select sum(minutes), goal_met()"
        ),
        record,
        POLICY,
    )
    first = result["rows"][0]  # March 3 week: days met, minutes not met
    listed = {
        "statements": [
            {
                "text": "Week of March 3: days goal met (2), minutes goal not met (75).",
                "kind": "value",
                "cites": [first["id"]],
            },
            {
                "text": "The goal changes its met/not-met status between the two readings.",
                "kind": "value",
                "cites": [first["id"]],
            },
        ]
    }
    assert not any("goal for" in i for i in code_check(listed, [result], record)[0])


def test_a_checklist_total_for_one_week_is_that_weeks_row():
    record = record_two_weeks()
    result = execute(
        parse(
            "from encounters where date >= 2026-03-03 and date <= 2026-03-16 and disposition = "
            "included group_by week select sum(minutes)"
        ),
        record,
        POLICY,
    )
    week1 = result["rows"][0]
    answer = {
        "statements": [
            {"text": "The week of March 3 had 75 minutes.", "kind": "value", "cites": [week1["id"]]}
        ]
    }
    need = [{"item": "Total minutes in the week of March 3-9", "query": 1}]
    issues, _ = code_check(answer, [result], record, required_totals=need)
    assert not any("combined figure" in i for i in issues)


def test_a_document_is_one_record_of_a_contact_whatever_else_it_carries():
    note = visit("A", "note", "V1", "2026-03-18", "09:00", "09:45")
    export = obs(
        "B",
        "note",
        "contact",
        [("encounter_id", "V1", "V1"), ("date", "2026-03-18", "2026-03-18")],
        evidence="reported",
        relation=Relation(type="addendum"),
    )
    record = build_record(docs("note", "plan"), goal() + [note, export], POLICY)
    records = record.facts_of("V1")["records"].value
    assert len(records) == 1 and records[0].endswith("(actual)")
