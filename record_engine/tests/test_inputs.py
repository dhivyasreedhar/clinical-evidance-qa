"""New or changed input documents, on the synthetic physical-therapy patient: equal-standing
attendance conflicts, another patient's document, one visit number used by two organisations,
an authorization that is not a goal, a later plan that replaces an earlier one, and prose checks
for goal outcomes, weekdays and the patient's identity. Offline, no model calls."""

from __future__ import annotations

from datetime import date

from record_engine import llm
from record_engine.model import Relation
from record_engine.qa import (
    CHECKLIST_ISSUE,
    PART_ISSUE,
    absence_in_facts,
    final_status,
    goal_outcome_issues,
    stated,
    weekday_issues,
)
from record_engine.query import execute, parse
from record_engine.reconcile import build_record
from record_engine.tests.test_engine import POLICY, docs, goal, obs, record_two_weeks, visit
from record_engine.values import parse_time

WEEKS = (
    "from encounters where date >= 2026-03-03 and date <= 2026-03-09 "
    "group_by week select count_distinct(date), sum(minutes), goal_met()"
)


def header(oid, doc, mrn, dob="1980-01-01", issuer="Riverside Physio"):
    return obs(
        oid,
        doc,
        "doc_meta",
        [
            ("issuer", issuer, issuer),
            ("patient_name", "Alex Kim", "Alex Kim"),
            ("patient_mrn", mrn, mrn),
            ("patient_dob", dob, dob),
        ],
    )


def test_equal_sources_disagreeing_about_attendance_make_the_goal_undeterminable():
    observations = goal() + [
        visit("A", "a", "V1", "2026-03-03", "09:00", "09:45"),
        visit("B1", "b1", "V2", "2026-03-05", "09:00", "09:40"),
        obs(
            "B2",
            "b2",
            "contact",
            [
                ("encounter_id", "V2", "V2"),
                ("date", "2026-03-05", "2026-03-05"),
                ("status_claim", "no_show", "no show"),
            ],
        ),
    ]
    record = build_record(docs("a", "b1", "b2", "plan"), observations, POLICY)
    # the query runs with an uncertain disposition, and the row says why
    rows = execute(parse("from encounters select rows()"), record, POLICY)["rows"][0]["rows()"]
    v2 = next(r for r in rows if r["id"] == "V2")
    assert v2["disposition"] == "uncertain" and v2["delivered"] == "uncertain"
    week = execute(parse(WEEKS), record, POLICY)["rows"][0]["goal_met()"]
    # 1 or 2 days, 45 or 85 minutes: neither threshold can be judged
    assert week["status"] == "cannot_determine"
    assert week["checks"][0]["attendance_uncertain"] == ["V2"]


def test_a_document_about_another_patient_is_set_aside():
    observations = goal() + [
        header("H1", "a", "PT-001"),
        header("H2", "b", "PT-001"),
        header("H3", "other", "PT-999", dob="1975-05-05"),
        visit("A", "a", "V1", "2026-03-03", "09:00", "09:45"),
        visit("B", "b", "V2", "2026-03-05", "09:00", "09:40"),
        visit("X", "other", "V9", "2026-03-04", "10:00", "11:00"),
    ]
    record = build_record(docs("a", "b", "other", "plan"), observations, POLICY)
    assert "V9" not in {e.id for e in record.events}
    aside = [o for o in record.open_items if o.kind == "other_patient"]
    assert [o.subject for o in aside] == ["other"] and "PT-999" in aside[0].text
    assert record.facts_of("patient")["patient_mrn"].value == "PT-001"
    total = execute(parse("from encounters select count()"), record, POLICY)["rows"][0]
    assert total["count()"] == 2


def test_one_visit_number_from_two_organisations_is_two_events():
    observations = goal() + [
        header("H1", "a", "PT-001"),
        header("H2", "b", "PT-001"),
        header("H3", "clinic", "PT-001", issuer="Northside Clinic"),
        visit("A", "a", "V1", "2026-03-03", "09:00", "09:45"),
        visit("B", "b", "V1", "2026-03-03", "09:00", "09:45"),
        obs(
            "C",
            "clinic",
            "contact",
            [
                ("encounter_id", "V1", "V1"),
                ("date", "2026-03-03", "2026-03-03"),
                ("service", "nutrition consult", "nutrition consult"),
                ("status_claim", "attended", "attended"),
                ("start", "15:00", "15:00"),
                ("end", "15:30", "15:30"),
            ],
        ),
    ]
    record = build_record(docs("a", "b", "clinic", "plan"), observations, POLICY)
    ids = {e.id for e in record.events if e.kind == "encounter"}
    assert ids == {"V1", "V1@northside-clinic"}
    assert record.facts_of("V1")["minutes"].value == 45
    assert record.facts_of("V1@northside-clinic")["disposition"].value == "excluded"


def test_an_authorization_is_not_a_goal_and_no_goal_counts_nothing():
    authorization = obs(
        "AU",
        "auth",
        "plan_goal",
        [
            ("basis", "authorization", "authorized"),
            ("threshold", "6", "6"),
            ("unit", "sessions", "sessions"),
            ("period", "episode", "episode"),
            ("eligible_services", "aquatic therapy", "aquatic therapy"),
        ],
    )
    observations = [authorization, visit("A", "a", "V1", "2026-03-03", "09:00", "09:45")]
    record = build_record(docs("a", "auth"), observations, POLICY)
    assert record.facts_of("V1")["disposition"].value == "attended_no_goal"
    with_goal = build_record(docs("a", "auth", "plan"), observations + goal(), POLICY)
    assert with_goal.facts_of("V1")["disposition"].value == "included"


def test_a_later_plan_replaces_an_earlier_goal_from_its_own_start():
    def minutes_goal(oid, doc, threshold, start, signed):
        return obs(
            oid,
            doc,
            "plan_goal",
            [
                ("threshold", threshold, threshold),
                ("unit", "minutes", "minutes"),
                ("comparator", "at_least", "at least"),
                ("period", "week", "week"),
                ("week_start", "tuesday", "Tuesday"),
                ("eligible_services", "physical therapy", "physical therapy"),
                ("effective_start", start, start),
            ],
            recorded=[signed],
        )

    observations = [
        minutes_goal("G1", "plan", "80", "2026-03-03", "2026-03-01"),
        minutes_goal("G2", "amend", "30", "2026-03-10", "2026-03-09"),
        visit("A", "a", "V1", "2026-03-03", "09:00", "09:45"),  # week 1: 45 < 80
        visit("B", "b", "V2", "2026-03-10", "09:00", "09:45"),  # week 2: 45 >= 30
    ]
    record = build_record(docs("a", "b", "plan", "amend"), observations, POLICY)
    rows = execute(
        parse(
            "from encounters where date >= 2026-03-03 and date <= 2026-03-16 "
            "group_by week select sum(minutes), goal_met()"
        ),
        record,
        POLICY,
    )["rows"]
    status = {r["group"]: r["goal_met()"]["status"] for r in rows if "goal_met()" in r}
    assert status == {"2026-03-03..2026-03-09": "not_met", "2026-03-10..2026-03-16": "met"}


def test_prose_goal_outcomes_must_match_the_per_threshold_result():
    row = {
        "id": "R1.4",
        "covered": "2026-03-10..2026-03-16",
        "goal_met()": {
            "status": "cannot_determine",
            "checks": [
                {"unit": "days", "outcome": "met"},
                {"unit": "minutes", "outcome": "cannot_determine"},
            ],
        },
    }
    wrong = "Both the days goal and the minutes goal cannot be determined."
    assert goal_outcome_issues(0, wrong, [row], None, None)
    right = "The days goal was met; the minutes goal cannot be determined."
    assert goal_outcome_issues(0, right, [row, dict(row, id="R2.4")], None, None) == []
    by_scenario = (
        "Under the 50-minute scenario the minutes goal is met. Under the 40-minute scenario "
        "the minutes goal is not met."
    )
    assert goal_outcome_issues(0, by_scenario, [row], None, None) == []


def test_each_clause_is_checked_against_the_week_it_names():
    def week(start, end, status):
        return {"id": f"R{start}", "covered": f"{start}..{end}", "goal_met()": {"status": status}}

    rows = [
        week("2026-03-02", "2026-03-08", "not_met"),
        week("2026-03-09", "2026-03-15", "met"),
        week("2026-03-16", "2026-03-22", "cannot_determine"),
    ]
    first, last = date(2026, 3, 2), date(2026, 3, 22)
    right = (
        "The goals were not met in every week: only the week of March 9–15 met the goal; the "
        "other weeks did not meet the goal."
    )
    assert goal_outcome_issues(0, right, rows, first, last) == []
    wrong = "The week of March 2–8 met the goal; the week of March 9–15 did not meet the goal."
    issues = goal_outcome_issues(0, wrong, rows, first, last)
    assert len(issues) == 2 and "2026-03-02" in issues[0] and "2026-03-09" in issues[1]
    # a clause naming no week refers to the one week the statement names
    assert goal_outcome_issues(
        0, "In the week of March 9, it did not meet the goal.", rows, first, last
    )


def test_a_numbered_range_of_list_items_is_not_a_value():
    numbers, _ = stated("Items remain: (1) a link; (2–4) three conflicts; (5) a gap.", [])
    assert numbers == set()


def test_a_weekday_beside_a_date_must_be_that_dates_weekday():
    assert weekday_issues(0, "Tuesday, March 3, 2026 and 2026-03-10 (Tuesday)", None, None) == []
    issues = weekday_issues(0, "March 7 is a Thursday.", None, None)
    assert issues and "Saturday" in issues[0]
    assert weekday_issues(0, "each Monday–Sunday week of March 2", None, None) == []


def test_an_absence_claim_about_the_patients_own_identifiers_is_checked():
    observations = [header("H1", "a", "PT-001"), header("H2", "b", "PT-001")]
    record = build_record(docs("a", "b"), observations, POLICY)
    hits = absence_in_facts("The record does not document an MRN.", record, POLICY)
    assert [f.field for f in hits] == ["patient_mrn"]
    assert absence_in_facts("No other MRN is documented.", record, POLICY) == []


def test_spellings_of_one_organisation_are_one_issuer():
    observations = goal() + [
        header("H1", "a", "PT-001", issuer="RIVERSIDE PHYSIO CLINIC"),
        header("H2", "b", "PT-001", issuer="RIVERSIDE PHYSIO CLINIC"),
        header("H3", "mail", "PT-001", issuer="Riversidephysio"),
        visit("A", "a", "V1", "2026-03-03", "09:00", "09:45"),
        visit("B", "b", "V2", "2026-03-05", "09:00", "09:40"),
        obs(
            "M",
            "mail",
            "contact",
            [
                ("encounter_id", "V2", "V2"),
                ("date", "2026-03-05", "2026-03-05"),
                ("status_claim", "no_show", "did not attend"),
            ],
            recorded=["2026-03-09"],
            relation=Relation(type="corrects", fields=["status_claim", "start", "end"]),
        ),
    ]
    record = build_record(docs("a", "b", "mail", "plan"), observations, POLICY)
    assert {e.id for e in record.events if e.kind == "encounter"} == {"V1", "V2"}
    assert record.facts_of("V2")["disposition"].value == "excluded"


def test_a_unit_of_an_organisation_is_the_same_issuer():
    # a scheduling export issued by "<organisation> | Appointment desk" lists the same visits
    observations = goal() + [
        header("H1", "a", "PT-001", issuer="RIVERSIDE PHYSIO CLINIC"),
        header("H2", "desk", "PT-001", issuer="Riverside Physio Clinic | Appointment desk"),
        visit("A", "a", "V1", "2026-03-03", "09:00", "09:45"),
        visit("B", "desk", "V1", "2026-03-03", "09:00", "09:45"),
    ]
    record = build_record(docs("a", "desk", "plan"), observations, POLICY)
    assert [e.id for e in record.events if e.kind == "encounter"] == ["V1"]


def test_a_stated_duration_restating_corrected_times_falls_with_them():
    observations = goal() + [
        visit("A", "a", "V1", "2026-03-03", "09:00", "09:45", recorded=["2026-03-03"]),
        obs(
            "B",
            "b",
            "contact",
            [
                ("encounter_id", "V1", "V1"),
                ("date", "2026-03-03", "2026-03-03"),
                ("service", "Physical therapy", "Physical therapy"),
                ("status_claim", "attended", "attended"),
                ("start", "09:15", "09:15"),
                ("end", "09:45", "09:45"),
                ("stated_minutes", "30", "30 minutes"),
            ],
            recorded=["2026-03-03"],
        ),
        obs(
            "C",
            "fix",
            "contact",
            [
                ("encounter_id", "V1", "V1"),
                ("date", "2026-03-03", "2026-03-03"),
                ("start", "09:00", "09:00"),
                ("end", "09:45", "09:45"),
            ],
            recorded=["2026-03-05"],
            # names only the start: the 30 minutes that restated 09:15-09:45 falls with it
            relation=Relation(type="corrects", fields=["start"]),
        ),
    ]
    record = build_record(docs("a", "b", "fix", "plan"), observations, POLICY)
    minutes = record.facts_of("V1")["minutes"]
    assert minutes.status != "conflicting" and minutes.value == 45


def test_undecided_wording_is_not_a_met_claim():
    row = {
        "id": "R1.3",
        "covered": "2026-03-10..2026-03-16",
        "goal_met()": {
            "status": "cannot_determine",
            "checks": [
                {"unit": "days", "outcome": "cannot_determine"},
                {"unit": "minutes", "outcome": "cannot_determine"},
            ],
        },
    }
    text = (
        "The unresolved attendance blocks both the days goal and the minutes goal, so neither "
        "can be confirmed as met or not met."
    )
    assert goal_outcome_issues(0, text, [row], None, None) == []
    assert goal_outcome_issues(0, "The days goal was met.", [row], None, None)


def test_a_goal_outcome_where_no_goal_is_documented_is_flagged():
    row = {"id": "R1.3", "covered": "2026-03-10..2026-03-16", "goal_met()": {"status": "no_goal"}}
    wrong = "Alex did not meet the weekly therapy goal in the week of March 10."
    issues = goal_outcome_issues(0, wrong, [row], None, None)
    assert issues and "no_goal" in issues[0]
    right = (
        "No care goal is documented, so whether the goal was met cannot be judged; "
        "documentation of a goal would be needed to assess whether the goal was met."
    )
    assert goal_outcome_issues(0, right, [row], None, None) == []
    met_row = {
        **row,
        "goal_met()": {"status": "met", "checks": [{"unit": "days", "outcome": "met"}]},
    }
    assert goal_outcome_issues(0, "The goal was not met that week.", [met_row], None, None)
    assert goal_outcome_issues(0, "Alex met the weekly goal.", [met_row], None, None) == []


def test_only_coverage_gaps_left_after_repair_publish_as_partial():
    gap = [PART_ISSUE + "minutes recorded", CHECKLIST_ISSUE + "minutes recorded"]
    assert final_status([], gap, "answered") == "partial"
    # the writer's own "partial" stands only when the answer states a gap
    assert final_status([], [], "partial", gaps_stated=False) == "answered"
    assert final_status([], [], "partial", gaps_stated=True) == "partial"
    assert final_status(["statement 0: number not in results"], gap, "answered") == "withheld"
    assert final_status([], ["statement 1 is not supported"], "answered") == "withheld"
    assert final_status([], [], "answered") == "answered"


def test_clock_times_with_seconds_and_iso_timestamps():
    assert parse_time("15:18:30") == "15:18"
    assert parse_time("2026-01-29T15:18:30Z") == "15:18"
    assert parse_time("3:05 pm") == "15:05"


def test_a_reimported_form_under_another_form_id_is_one_administration():
    def form(oid, doc, form_id, day, score):
        return obs(
            oid,
            doc,
            "measurement",
            [
                ("instrument", "PHQ-9", "PHQ-9"),
                ("form_id", form_id, form_id),
                ("completed_on", day, day),
                ("score", str(score), str(score)),
            ],
        )

    observations = [
        form("M1", "a", "Q-116", "2026-03-06", 14),
        form("M2", "b", "F-0116", "2026-03-06", 14),
        form("M3", "b", "F-0117", "2026-03-06", 9),
    ]
    record = build_record(docs("a", "b"), observations, POLICY)
    ids = [e.id for e in record.events if e.kind == "measurement"]
    # one administration re-imported, one second administration that day: two distinct events
    assert len(ids) == 2 and len(set(ids)) == 2
    assert any("form IDs F-0116, Q-116" in o.text for o in record.open_items)


def test_usage_scopes_nest_and_reach_worker_threads():
    from concurrent.futures import ThreadPoolExecutor

    with llm.scope() as outer:
        with llm.scope() as inner:
            with ThreadPoolExecutor(2) as pool:
                list(pool.map(llm.carry(lambda _: llm._record("t", "m", None, True)), range(3)))
    assert inner.as_dict() == outer.as_dict()
    assert outer.as_dict() != llm.Usage().as_dict()


def test_an_addendum_that_names_the_fields_it_changes_is_a_correction():
    first = visit("A", "note", "V1", "2026-03-03", "09:10", "09:50", recorded=["2026-03-03"])
    other = visit("B", "other", "V1", "2026-03-03", "09:00", "09:50", recorded=["2026-03-03"])
    late = visit(
        "L",
        "late",
        "V1",
        "2026-03-03",
        "09:00",
        "09:50",
        recorded=["2026-03-05"],
        relation=Relation(type="addendum", fields=["start"], quote="arrived 9:00", block="late:L1"),
    )
    record = build_record(
        docs("note", "other", "late", "plan"), goal() + [first, other, late], POLICY
    )
    start = record.facts_of("V1")["presence_start"]
    assert (start.value, start.rule) == ("09:00", "signed_correction_supersedes_original")
    assert record.facts_of("V1")["minutes"].value == 50.0


def test_a_correction_signed_by_a_person_joins_the_record_it_corrects():
    roster = visit("R", "roster", "V2", "2026-03-05", "10:30", "11:30")
    email_header = obs(
        "H",
        "email",
        "doc_meta",
        [("issuer", "Dana Ross, PT", "Dana Ross, PT"), ("title", "Correction", "Correction")],
    )
    fix = obs(
        "F",
        "email",
        "contact",
        [
            ("encounter_id", "V2", "V2"),
            ("date", "2026-03-05", "2026-03-05"),
            ("status_claim", "no_show", "did not attend"),
            ("patient_present", "no", "no patient contact"),
        ],
        recorded=["2026-03-06"],
        relation=Relation(
            type="corrects", fields=["status_claim"], quote="did not", block="email:L1"
        ),
    )
    others = [header(f"H{n}", d, "RP-1") for n, d in enumerate(["roster", "plan"])]
    record = build_record(
        docs("roster", "email", "plan"), goal() + others + [roster, email_header, fix], POLICY
    )
    ids = [e.id for e in record.events if e.kind == "encounter"]
    assert ids == ["V2"]  # one event, not V2 and V2@dana-ross
    assert record.facts_of("V2")["attendance"].value == "not_attended"


def test_what_an_encounter_count_counted_is_worked_out_by_code():
    from record_engine.qa import counted

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
    seen = visit("A", "note", "V1", "2026-03-19", "09:00", "09:45")
    record = build_record(docs("log", "note", "plan"), goal() + [missed, seen], POLICY)
    everything = execute(parse("from encounters select count()"), record, POLICY, "R1")
    received = execute(
        parse("from encounters where delivered = yes select count()"), record, POLICY, "R2"
    )
    assert "did not receive (no show 1)" in counted(everything, record)
    assert counted(received, record).endswith("all received by the patient")
    measures = {"source": "measurements", "rows": [{"members": ["x"]}]}
    assert counted(measures, record) == ""


def test_a_count_audit_lists_what_the_count_left_out_and_every_row_must_be_explained():
    from record_engine.qa import COVERAGE_ISSUE, audit_coverage, count_audit

    missed = obs(
        "M",
        "log",
        "contact",
        [
            ("encounter_id", "V9", "V9"),
            ("date", "2026-03-19", "2026-03-19"),
            ("service", "Physical therapy", "Physical therapy"),
            ("status_claim", "no_show", "no show"),
        ],
    )
    first = visit("A", "note1", "V1", "2026-03-18", "09:00", "09:45")
    second = visit("B", "note2", "V2", "2026-03-20", "09:00", "09:45")
    same_day = visit("C", "note3", "V3", "2026-03-20", "14:00", "14:30")
    record = build_record(
        docs("log", "note1", "note2", "note3", "plan"),
        goal() + [missed, first, second, same_day],
        POLICY,
    )
    counted = execute(
        parse("from encounters where delivered = yes select count()"), record, POLICY, "R1"
    )
    audit = count_audit([counted], record)
    kinds = {row["kind"]: row["members"] for row in audit["rows"]}
    assert kinds["booked visits the patient did not attend (no-show)"] == ["V9"]
    assert kinds["more than one counted visit on 2026-03-20"] == ["V2", "V3"]
    answer = {"statements": [{"text": "V9 was a no-show.", "cites": ["V9"]}]}
    gaps = audit_coverage(answer, [counted, audit])
    assert gaps and all(g.startswith(COVERAGE_ISSUE) for g in gaps)
    assert not any("no-show" in g for g in gaps)
    answer["statements"].append(
        {"text": "Two visits on March 20.", "cites": [audit["rows"][-1]["id"]]}
    )
    assert audit_coverage(answer, [counted, audit]) == []


def test_the_records_internal_vocabulary_is_a_style_finding():
    from record_engine.qa import STYLE_ISSUE, jargon

    record = record_two_weeks()
    plain = {"statements": [{"text": "The two notes give different start times.", "cites": []}]}
    assert jargon(plain, record) == []
    internal = {
        "statements": [
            {
                "text": "presence_start is conflicting (OI-3) under the single_source rule.",
                "cites": [],
            },
            {"text": "Two open items remain; the fact fields have documented status.", "cites": []},
        ]
    }
    found = jargon(internal, record)
    assert len(found) == 2 and all(f.startswith(STYLE_ISSUE) for f in found)
    assert "OI-3" in found[0] and "presence_start" in found[0]


def test_a_count_written_as_a_word_is_checked_like_a_digit():
    numbers, _ = stated("Seven disagreements remain; the two notes agree; twenty-one days.", [])
    assert numbers == {7.0, 21.0}


def test_a_count_that_introduces_a_list_must_match_the_items_listed():
    from record_engine.qa import list_count_issues

    ids = {"V1", "V2", "V3"}
    wrong = "Five visits were not counted: a no-show (V1), a cancellation (V2), and a draft (V3)."
    assert list_count_issues(0, wrong, ids)
    assert list_count_issues(0, wrong.replace("Five", "Three"), ids) == []
    # an item without its own record: the list is not counted by code
    unnamed = "Four contacts were excluded: a call (V1), a notice (V2), and a portal review."
    assert list_count_issues(0, unnamed, ids) == []


def test_statements_code_still_flags_are_removed_not_rewritten():
    from record_engine.qa import without_flagged

    record = record_two_weeks()
    fact = next(f.id for f in record.facts if f.field == "service")
    answer = {
        "statements": [
            {"text": "Visits were attended.", "kind": "narrative", "cites": [fact]},
            {"text": "There were 99 visits.", "kind": "value", "cites": []},
        ]
    }
    issues = ["statement 1: 99 is in no cited result"]
    reduced, left, removed = without_flagged(answer, issues, [], record, {}, "", None)
    assert [s["text"] for s in reduced["statements"]] == ["Visits were attended."]
    assert left == [] and removed == ["There were 99 visits."]
    # a finding not tied to one statement removes nothing
    same, left, removed = without_flagged(
        answer, issues + ["required total missing"], [], record, {}, "", None
    )
    assert same is answer and removed == []


def test_a_statement_the_review_finds_unsupported_is_removed_with_the_code_flagged_ones():
    from record_engine.qa import REVIEW, without_flagged

    record = record_two_weeks()
    fact = next(f.id for f in record.facts if f.field == "service")
    answer = {
        "statements": [
            {"text": "Visits were attended.", "kind": "narrative", "cites": [fact]},
            {
                "text": "The visit was a copy of a corrected note.",
                "kind": "narrative",
                "cites": [fact],
            },
            {"text": "There were 99 visits.", "kind": "value", "cites": []},
        ]
    }
    flags = ["statement 2: 99 is in no cited result", f"{REVIEW}statement 1: not supported"]
    reduced, left, removed = without_flagged(answer, flags, [], record, {}, "", None)
    assert [s["text"] for s in reduced["statements"]] == ["Visits were attended."]
    assert left == [] and len(removed) == 2


def test_the_answer_prompt_names_the_count_list_by_its_purpose():
    from record_engine.qa import ANSWER, AUDIT_PURPOSE

    assert AUDIT_PURPOSE in ANSWER


def test_negated_goal_outcomes_read_as_not_met():
    from record_engine.qa import goal_claims

    for text in (
        "The days goal has not been met.",
        "The days goal wasn't met.",
        "The days goal was never met.",
    ):
        assert goal_claims(text) == {"days": {"not_met"}}
