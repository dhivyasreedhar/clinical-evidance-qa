"""⑥ plan → ⑦ execute → ⑧ answer → ⑨ check → ⑩ frame.

Plan (planner model): the question becomes queries in the record's query language plus a
checklist of what a complete answer must state. Execute (code): results with scenarios and
provenance; a query that fails to parse or type-check gets one retry with the error. Answer
(writer model): typed statements citing fact, result and passage IDs. Check: code first (every
number and time bound to a cited value, required totals, goal outcomes, weekdays, list counts,
status of conflicting and missing facts), then the small model (question parts, checklist,
populations, support of reasons and descriptions), then every "not documented" claim is verified
against the facts and the sources. A population mismatch re-plans once; up to two repairs follow.
Statements still flagged are removed (never rewritten) and the rest re-checked; an answer whose
code findings cannot be resolved that way is withheld with the reasons. Frame: the small model
picks and orders the checked statements that answer the question. Each further model step starts
only when the answer's time budget covers it. The model review never overrules a code finding.
"""

from __future__ import annotations

import json
import re
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
from typing import Any

from record_engine import llm
from record_engine import query as dsl
from record_engine.dates import date_spans, find_dates
from record_engine.evidence import PassageIndex, verify_absence
from record_engine.ingest import Document
from record_engine.model import Record
from record_engine.policy import Policy
from record_engine.values import NUMBER, TIME, parse_time

# Prefixes of the findings the checks produce; final_status and the repair loop match on them.
PART_ISSUE = "part of the question not answered: "
REVIEW = "review: "  # marks a review finding passed along with code findings
COVERAGE_ISSUE = "a kind of record the count audit lists is not explained: "
STYLE_ISSUE = "plain language: "
POPULATION_ISSUE = "population does not match the question: "
CHECKLIST_ISSUE = "checklist item not addressed: "

PLAN = """You turn a question about one patient's record into queries for a small query language,
and a checklist. You never answer the question yourself.

Query language:
{grammar}

Record catalogue (what exists; use these field values exactly):
{catalogue}

Write 1-5 queries whose results together hold every number, list and fact the answer needs:
- counts, days, minutes and goal status come from queries (never from judgement); to count
  delivered therapy toward a goal filter disposition = included (it already means attended and
  an eligible service); goal_met() needs group_by week, and is selected only when the question
  asks about goals, targets or whether care met a requirement;
- for "which/list/what happened" questions, list the rows (select list(...) or rows()) so the
  answer can enumerate them, including excluded/cancelled/absent ones when relevant;
- for narrative questions (symptoms, strategies, functioning, safety, reports), query findings
  filtered by type, reporter, date or text (contains), with rows();
- sessions, visits, days or minutes of care count care the patient received (delivered = yes;
  for goal-eligible therapy, disposition = included); missed, cancelled and patient-absent
  bookings are counted only when the question asks about appointments, bookings, attendance
  outcomes or every contact;
- to show what counts and what does not, query without the disposition filter and list rows;
- measurement changes: filter to the instrument and to total scores (item = none) and use
  change()/percent_change();
- conflicts and gaps: from open_items or from facts where status = conflicting;
- rows() shows each item's supporting documents and their role (copy, superseded,
  contradicts), which answers duplicate/copy/correction questions.
For each query state its population in plain words: which records it counts or lists (for
example "all attended visits of any service", "goal-eligible therapy visits", "PHQ-9 total
scores"). Choose the population the question asks about, not a narrower or wider one; when the
question names dates, every named date must fall inside some query's date window.
For every checklist item that asks for a combined figure (a total, a combined result, a
reconciliation across records, a sum across weeks or services), write a query that computes it
and list it under required_totals with that query's number (1 = the first query).
Checklist: the short items a complete answer must state, taken only from what the question
asks, in the question's words (never about query fields, codes or the record's internals). One
item per thing the question asks: a question that asks one thing gets one item (at most 6).
Never add background, treatment, course or outcome items the question does not ask for.
explain_counts: true only when the question itself asks which records were excluded, could be
counted twice or are ineligible for a count; code then adds a list of every such record. False
for questions that only ask for totals, calculations, goals or what happened on given dates.
answerable: yes, partially, or no (with the reason) given what the catalogue contains."""

ANSWER = """You answer a question about one patient's record using ONLY the supplied query results,
facts and open items. The facts are the reconciled record around the question (every field of the
events it names or the results return, and findings on its dates); use them for what the query
results do not show. Code computed every number; you never count, add, subtract or convert beyond minutes to
hours (100 minutes = 1 h 40 min).

You also get passages: source text found by searching the documents for the question's words.
Use them for anything the results do not hold (names, reasons, what a document says), and cite
them by their id. Before saying the record does not document something, check the passages.

Return typed statements. Each statement cites the IDs it rests on: result IDs (R1) or result row IDs
(R1.2), fact IDs (F-1a2b3c4d), open item IDs (OI-3), record item IDs shown in the rows (an encounter, measurement or
finding id) or passage ids. Cite the specific rows/items a number comes from. Kinds:
- value: a documented or computed value; every number/time in it must come from a cited row/fact.
- conflict: sources disagree; name every scenario (e.g. "40 or 50 minutes") and the sources.
- missing: the record does not document it; say what documentation would settle it.
- inference: a conclusion drawn from cited facts; say it is an inference.
- narrative: what the notes say (symptoms, strategies, functioning...), citing the finding facts.
Every count, total, difference or percentage you state must appear in a cited result; the only
count you may state yourself is the number of items you cite in that same statement. If a figure
you want is not in the results (for example a change between two middle administrations), leave
it out. A grouped result ends with an "all groups" row holding totals across its groups (for
example distinct days across weeks); use it instead of adding groups up. Describe dispositions and statuses in plain words (excluded, not attended, no record of
what happened), never as code values.
Speak about the patient's record, never about this system: do not mention results, queries,
computed figures, IDs or what is "available in the results"; a "missing" statement says what the
record does not document and what documentation would settle it.
Status: "answered" when every part of the question gets an answer, including one given as the
scenarios of a conflict; "partial" only when the record does not document something a part of the
question needs (a "missing" statement then says what); "unsupported" when it documents none of it.
Rules: address every checklist item; enumerate every member of a list the question asks for;
never present a conflicting fact as a single value; never assert a fact whose status is
not_documented. When the question asks about goals, state goal status per threshold exactly as
computed (by_threshold: each threshold's measured value and outcome — met, not met, cannot be
determined), then the overall status, and note a partial week; otherwise leave goals out.
Answer the question that was asked, directly: the first statement is the answer. Add only what
the question asks for or what is needed to read the answer correctly (a conflict, a gap, a
partial week); no background, treatment details, course or outcomes the question did not ask
about. A question about one thing gets 1-3 statements; a list the question asks for is given in
full; never more than 8 statements, each under 70 words.
Say which population every count or total covers (for example "all attended visits, including
medication management" or "therapy sessions that count toward the goal"). When the question's
words fit more than one population, answer for the one the words name most directly and name
what it includes.
Never mention
internal IDs (R1.2, F-...) or file names in the text; cite them in cites.
Write for a clinician, in plain words. Never write the record's internal vocabulary: field names
(presence_start, stated_minutes), rule names (single_source), item kinds (reading_disagreement,
candidate_link), code values, or labels such as "documented status", "open item", "fact field".
Say what they mean instead: "the two notes give different start times", "may be the same visit",
"one source records this".
Describe a document by what its passage says. The role after a document's title (actual,
reported, copy, addendum, planned, billed, corrects) is how the record classified it: say it in
plain words (a copy, a correction, a draft, a billing record), and when two readings of that
document disagree, the classification is unsettled: describe the document from its passage, not
from the label. Notes that two readings of a document disagree, or that a mention was not
captured, are review notes about how the documents were read, not facts about the patient's care:
mention them only when the question asks what is unresolved or needs review.
A result whose purpose is "records a count left out or that could change it" lists, one row per
kind, every such record: bookings not received, received services the count does not include,
contacts without a visit number, documents that repeat or restate a counted visit (copies,
corrections, drafts, billing, exports listing several visits), and days with more than one
counted visit. When it is supplied, explain every row in plain words (what the records are, and
whether and why they are or are not counted), citing the row; do not call it an audit or a
result."""

CHECK = """You check an answer against its question and its evidence. First split the question
into its separate parts (each thing it asks for: every count, total, date, comparison, list,
explanation) and say for each part whether the answer addresses it with a concrete answer: a
figure, a list, or an explicit statement that the record does not document it. A statement that
the record does not document something, or that it cannot be determined, fully addresses that
part; do not require information the record does not contain. Then, for each
checklist item, say whether the answer addresses it. For each listed statement, say whether its cited evidence supports it (for a
"missing" statement: the evidence must not document what it says is missing): every
clinical claim in the statement must be stated by at least one cited passage or value (faithful
paraphrase is fine; a claim that only shares the topic is not supported). Judge each independently.
Read a long statement clause by clause: every reason, status, list item and description of a
document (what it is, what it contains, what it changes) is a claim of its own. One such clause
that no evidence states, or that the evidence contradicts, makes the whole statement unsupported:
say which clause in why, quoting the evidence that contradicts it. A clause saying something is
not documented, not recorded or not a separate item is checked separately against the record and
the sources; do not judge it here. Numbers, counts, dates, times
and durations are verified by code against the record (including values code derived, such as
the time a patient was present); do not judge them.
A claim about what a document is or contains (an addendum, a copy, an attachment, what it
records) is supported only by that document's own passage or by fact values quoting it; a role
label or a note that two readings disagree does not support it, and a passage supports it only
when it comes from that same document (its id starts with that document's name): a passage from
another document with a similar role (another copy, another receipt) does not.
Finally, for each query result that a count, total or number of minutes in the answer is taken
from, say whether its population (what it counts) is the one the question asks that figure
about; a narrower or wider population (for example goal-eligible visits when the question asks
for all attended visits, or a different week) does not match. Judge the population from what
the result counted (its "counted" note, worked out by code), not only from its label: sessions,
visits, days or minutes of care that include bookings the patient did not receive (no-shows,
cancellations, patient absent) do not match a question about care, sessions or visits, unless the
question asks about appointments, bookings or every contact. Results that only list what is
excluded, give context or explain are not judged: leave them out."""


def catalogue(record: Record, policy: Policy) -> str:
    rows = {
        s: dsl.rows_for(s, record)
        for s in ("encounters", "measurements", "medications", "findings", "goals")
    }
    dates = sorted(r["date"] for r in rows["encounters"] if r.get("date"))

    def distinct(source: str, field: str) -> list[str]:
        return sorted({str(r.get(field)) for r in rows[source] if r.get(field) is not None})

    starts = [f.value for f in record.facts if f.field == "effective_start" and f.value]
    ends = [f.value for f in record.facts if f.field == "effective_end" and f.value]
    review = (
        f"review period (from the plan/goal documents): {max(set(starts), key=starts.count)} to "
        f"{max(set(ends), key=ends.count)}"
        if starts and ends
        else "review period: not stated"
    )
    lines = [
        review,
        f"encounters: {len(rows['encounters'])} rows, dates {dates[0] if dates else '?'} to {dates[-1] if dates else '?'}; "
        f"fields id, date, service {distinct('encounters', 'service')}, attendance {distinct('encounters', 'attendance')}, "
        f"disposition {distinct('encounters', 'disposition')} (included = attended and counts toward the goal; attended_no_goal = attended, but no documented care goal says which services count, so nothing is counted toward a goal), minutes (patient's creditable), session_minutes (documented session time whoever was present), scheduled (booked time), participants, mode, delivered (yes = the patient received the service, including partial attendance; no; uncertain = sources disagree), appointment_status {distinct('encounters', 'appointment_status')} (what happened to the booking: attended, partial, no_show, cancelled_by_patient, cancelled_by_clinic, ...), status_reason, status (certainty of the row's values), records (documents and their role: actual, reported, planned, templated, billed, authorized, copy, corrects, addendum), documents (IDs of every document that records the item: the linked-document group), weekday (computed), sources",
        f"measurements: {len(rows['measurements'])} rows; fields id, instrument {distinct('measurements', 'instrument')}, "
        f"item {distinct('measurements', 'item')} (none = total score), score, date, status, sources",
        f"references: {len(dsl.rows_for('references', record))} rows (entries that document no visit: bookings, templates, charges, references to visits recorded elsewhere, chart handling); fields id, date, service, kind, why, sources",
        f"charges: {len(dsl.rows_for('charges', record))} rows; fields id, charge_id, encounter_id, service, code, quantity, status, amount, date",
        f"medications: {len(rows['medications'])} rows; fields id, name, dose, schedule, change, date",
        f"findings: {len(rows['findings'])} rows; fields id, text, type {distinct('findings', 'type')}, reporter "
        f"{distinct('findings', 'reporter')}, date, encounter_id",
        "goals (fields id, basis, target, threshold, comparator, unit, period, week_start, "
        "eligible_services, excluded_services, effective_start, effective_end, sources; only "
        "basis treatment_goal or program_rule is a care goal that goal_met() judges; an "
        "authorization or payer limit caps what is covered and is never the goal): "
        + "; ".join(
            f"[{r.get('basis') or 'goal'}] {r.get('comparator')} {r.get('threshold')} {r.get('unit')} per {r.get('period')} (week starts {r.get('week_start')}; services {r.get('eligible_services')}; effective {r.get('effective_start')} to {r.get('effective_end')}; from {', '.join(x.split(' (')[0] for x in (r.get('sources') or []))})"
            for r in rows["goals"]
        ),
        "goal.services = " + ", ".join(sorted(dsl.goal_services(record, policy))),
        f"facts: {len(record.facts)} rows; fields id, subject, field, value, status {sorted({f.status for f in record.facts})}, rule, date",
        f"open_items: {len(record.open_items)} rows; kinds {sorted({o.kind for o in record.open_items})}",
    ]
    return "\n".join(lines)


PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "queries": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "purpose": {"type": "string"},
                    "population": {"type": "string"},
                    "query": {"type": "string"},
                },
                "required": ["purpose", "population", "query"],
            },
        },
        "checklist": {"type": "array", "items": {"type": "string"}},
        "required_totals": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"item": {"type": "string"}, "query": {"type": "integer"}},
                "required": ["item", "query"],
            },
        },
        "answerable": {"type": "string", "enum": ["yes", "partially", "no"]},
        "reason": {"type": "string"},
        "explain_counts": {"type": "boolean"},
    },
    "required": ["queries", "checklist", "answerable"],
}
ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["answered", "partial", "unsupported"]},
        "statements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "kind": {
                        "type": "string",
                        "enum": ["value", "conflict", "missing", "inference", "narrative"],
                    },
                    "cites": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["text", "kind", "cites"],
            },
        },
    },
    "required": ["status", "statements"],
}
CHECK_SCHEMA = {
    "type": "object",
    "properties": {
        "question_parts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"part": {"type": "string"}, "addressed": {"type": "boolean"}},
                "required": ["part", "addressed"],
            },
        },
        "checklist": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"item": {"type": "string"}, "addressed": {"type": "boolean"}},
                "required": ["item", "addressed"],
            },
        },
        "statements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer"},
                    "supported": {"type": "boolean"},
                    "why": {"type": "string"},
                },
                "required": ["index", "supported"],
            },
        },
    },
    "required": ["question_parts", "checklist", "statements"],
}
CHECK_SCHEMA["properties"]["populations"] = {  # type: ignore[index]
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "result": {"type": "string"},
            "matches": {"type": "boolean"},
            "why": {"type": "string"},
        },
        "required": ["result", "matches"],
    },
}


# --- ⑥ plan + ⑦ execute ---------------------------------------------------------------------


def window_errors(question: str, plan: dict[str, Any], record: Record) -> list[str]:
    """Every date the question names must fall inside some query's date window (a query with no
    date condition covers every date)."""
    days = sorted(str(f.value)[:10] for f in record.facts if f.field == "date" and f.value)
    if not days:
        return []
    first, last = date.fromisoformat(days[0]), date.fromisoformat(days[-1])
    named = sorted(find_dates(question, first, last, expand=False))
    if not named:
        return []
    windows = []
    parsed = 0
    for item in (plan.get("queries") or [])[:5]:  # only the first five are run
        text = item.get("query") if isinstance(item, dict) else item
        try:
            query = dsl.parse(str(text))
        except dsl.QueryError:
            continue
        parsed += 1
        window = [c for c in query.where if isinstance(c, dsl.Condition) and c.field == "date"]
        if not window:
            return []
        windows.append(dsl._window_bounds(window))
    if not parsed:
        return []  # the parse errors are reported on their own
    return [
        f"the question names {d.isoformat()} but no query's date window includes it; widen a "
        f"window or add a query that covers it"
        for d in named
        if not any((lo is None or lo <= d) and (hi is None or d <= hi) for lo, hi in windows)
    ]


def plan_and_execute(
    question: str, record: Record, policy: Policy, feedback: list[str] | None = None
) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    system = PLAN.format(grammar=dsl.__doc__, catalogue=catalogue(record, policy))
    prompt = question
    if feedback:
        prompt += "\n\nA check of an earlier plan found:\n" + "\n".join(feedback)
    plan = llm.call("plan", system, prompt, PLAN_SCHEMA, llm.PLANNER, 4000)
    results, errors = _run(plan, record, policy)
    errors += window_errors(question, plan, record)
    if errors:
        retry = llm.call(
            "plan-retry",
            system,
            f"{prompt}\n\nYour previous queries failed:\n"
            + "\n".join(errors)
            + "\nReturn corrected queries.",
            PLAN_SCHEMA,
            llm.PLANNER,
            4000,
        )
        plan = {**retry, "retried": True}
        results, errors = _run(plan, record, policy)
        errors += window_errors(question, plan, record)
        if results and errors and all("date window" in e for e in errors):
            plan["window_warnings"] = errors  # the queries run; the gap is reported, not fatal
            errors = []
    return plan, results, errors


def counted(result: dict[str, Any], record: Record) -> str:
    """What an aggregate over encounters counted, in code's words: how many of its items the
    patient did not receive, by booking outcome. A label can say "attended visits" while the
    query counted no-shows; this note says what was actually counted."""
    if result.get("source") != "encounters":
        return ""
    members = {m for row in result.get("rows", []) for m in row.get("members", [])}
    if not members:
        return ""
    rows = {r["id"]: r for r in dsl.rows_for("encounters", record)}
    missed = Counter(
        str(rows[m].get("appointment_status") or "unknown")
        for m in members
        if m in rows and rows[m].get("delivered") != "yes"
    )
    if not missed:
        return f"{len(members)} encounters, all received by the patient"
    detail = ", ".join(f"{k.replace('_', ' ')} {n}" for k, n in sorted(missed.items()))
    return (
        f"{len(members)} encounters, of which {sum(missed.values())} the patient did not "
        f"receive ({detail})"
    )


def _run(
    plan: dict[str, Any], record: Record, policy: Policy
) -> tuple[list[dict[str, Any]], list[str]]:
    results, errors = [], []
    for n, item in enumerate((plan.get("queries") or [])[:5], start=1):
        if isinstance(item, str):
            item = {"purpose": "", "query": item}
        if not isinstance(item, dict) or not isinstance(item.get("query"), str):
            errors.append(f"query {n} is not a query string")
            continue
        try:
            result = dsl.execute(dsl.parse(item["query"]), record, policy, f"R{n}")
            result["purpose"] = item.get("purpose", "")
            result["population"] = item.get("population", "")
            if note := counted(result, record):
                result["counted"] = note
            results.append(result)
        except dsl.QueryError as error:
            errors.append(f"{item['query']!r}: {error}")
    return results, errors


# --- count audit: what a count left out and what could change it ------------------------------

AUDIT_PURPOSE = "records a count left out or that could change it"
# the question's own words must ask for it: the planner alone over-applies the list to questions
# that only ask for totals
EXPLAIN_COUNTS = re.compile(
    r"\b(?:duplicat\w*|double[- ]count\w*|counted twice|ineligib\w*|exclu\w*|left out|not counted|"
    r"(?:inflate|overstate|overcount)\w*)",
    re.I,
)
_ROLE_WORDS = {
    "copy": "copies of a record already counted",
    "reported": "records reporting a visit documented elsewhere",
    "addendum": "attachments or addenda to a visit's record",
    "corrects": "corrections to a counted visit's record",
    "planned": "drafts, schedules or templates written before or without the visit",
    "templated": "drafts, schedules or templates written before or without the visit",
    "billed": "billing records",
}
_NOT_RECEIVED = {
    "no_show": "booked visits the patient did not attend (no-show)",
    "cancelled_by_clinic": "visits the clinic cancelled",
    "cancelled_by_patient": "visits the patient cancelled",
    "not_present": "contacts held without the patient present",
}


def count_audit(results: list[dict[str, Any]], record: Record) -> dict[str, Any] | None:
    """Every record that an encounter count left out or that could change it, one row per kind,
    worked out by code from the record: bookings not received, received services outside the
    count, contacts without a visit number, documents that repeat or restate a counted visit,
    documents that list several visits, and days with more than one counted visit. A question
    that asks what could be double-counted or is ineligible is answered from every row."""
    # the count being explained: the narrowest encounter count among the results (a listing of
    # every encounter, or a wider context count, is not what was counted)
    counts = [
        {m for row in r.get("rows", []) for m in row.get("members", [])}
        for r in results
        if r.get("source") == "encounters"
        and r.get("purpose") != AUDIT_PURPOSE
        and any(
            k.startswith(("count(", "count_distinct(", "sum("))
            for row in r.get("rows", [])
            for k in row
        )
    ]
    counts = [c for c in counts if c]
    if not counts:
        return None
    counted_ids = min(counts, key=len)
    rows = dsl.rows_for("encounters", record)
    by_id = {r["id"]: r for r in rows}
    days = sorted(str(by_id[m]["date"]) for m in counted_ids if m in by_id and by_id[m].get("date"))
    first, last = (days[0], days[-1]) if days else ("", "")
    # contacts without a date can be placed only in a count that spans the whole record
    dated = sorted(str(r["date"]) for r in rows if r.get("date"))
    whole = bool(dated) and first <= dated[0] and last >= dated[-1]
    window = [
        r
        for r in rows
        if r["id"] in counted_ids
        or (not r.get("date") and whole)
        or (r.get("date") and first <= str(r["date"]) <= last)
    ]
    groups: dict[str, list[str]] = {}
    documents: dict[str, set[str]] = defaultdict(set)
    for r in window:
        if r["id"] in counted_ids:
            continue
        if not str(r.get("date") or ""):
            groups.setdefault("contacts without a visit number or date", []).append(r["id"])
        elif r.get("delivered") != "yes":
            status = str(r.get("appointment_status") or "unknown")
            label = _NOT_RECEIVED.get(status, f"bookings not received ({status.replace('_', ' ')})")
            groups.setdefault(label, []).append(r["id"])
        else:
            groups.setdefault(
                f"received services this count does not include ({r.get('service')})", []
            ).append(r["id"])
    titles = {d["key"]: (d.get("title") or d["key"]) for d in record.documents}
    lists: dict[str, set[str]] = defaultdict(set)
    for r in window:
        for source in r.get("sources") or []:
            lists[str(source).rpartition(" (")[0]].add(r["id"])
        for record_label in r.get("records") or []:
            title, _, roles = str(record_label).rpartition(" (")
            for role in roles.rstrip(")").split(", "):
                if role in _ROLE_WORDS:
                    label = _ROLE_WORDS[role]
                    groups.setdefault(label, [])
                    if r["id"] not in groups[label]:
                        groups[label].append(r["id"])
                    documents[label].add(title)
    for key, listed in sorted(lists.items()):
        if len(listed) >= 3:
            label = f"one document lists several visits ({titles.get(key, key)})"
            groups[label] = sorted(listed)
            documents[label].add(titles.get(key, key))
    # a billing record of a visit in the period, counted or not, says nothing about attendance
    in_window = {r["id"] for r in window}
    for event in record.events:
        if event.kind == "charge":
            facts = record.facts_of(event.id)
            visit = facts.get("encounter_id")
            if visit is not None and str(visit.value) in in_window:
                label = _ROLE_WORDS["billed"]
                groups.setdefault(label, [])
                if str(visit.value) not in groups[label]:
                    groups[label].append(str(visit.value))
                documents[label] |= {
                    titles.get(e.block.split(":", 1)[0], e.block.split(":", 1)[0])
                    for f in facts.values()
                    for e in f.evidence
                }
    per_day: dict[str, list[str]] = defaultdict(list)
    for m in sorted(counted_ids):
        if m in by_id and by_id[m].get("date"):
            per_day[str(by_id[m]["date"])].append(m)
    for day, same_day in sorted(per_day.items()):
        if len(same_day) > 1:
            groups[f"more than one counted visit on {day}"] = same_day
    if not groups:
        return None
    n = len(results) + 1
    audit_rows = []
    for k, (label, members) in enumerate(groups.items(), start=1):
        audit_rows.append(
            {
                "id": f"R{n}.{k}",
                "kind": label,
                "members": members,
                "count": len(members),
                "items": [
                    {
                        key: by_id[m].get(key)
                        for key in ("id", "date", "service", "appointment_status", "status_reason")
                        if m in by_id
                    }
                    for m in members
                ],
                "documents": sorted(documents.get(label, set())),
            }
        )
    return {
        "id": f"R{n}",
        "query": "(code) records the count left out or that could change it",
        "source": "encounters",
        "purpose": AUDIT_PURPOSE,
        "population": "every encounter in the counted period and every document recording one",
        "rows": audit_rows,
        "excluded": [],
        "scenarios_are_range_endpoints": False,
    }


def audit_coverage(answer: dict[str, Any], results: list[dict[str, Any]]) -> list[str]:
    """Every row of a supplied count audit must be explained by some statement (cited by its row
    or by one of its records); a missing row is a coverage gap."""
    audit = next((r for r in results if r.get("purpose") == AUDIT_PURPOSE), None)
    if audit is None:
        return []
    statements = answer.get("statements", [])
    cited = {c for st in statements for c in st.get("cites", [])}
    known = sorted(
        date.fromisoformat(str(i["date"])[:10])
        for row in audit["rows"]
        for i in row.get("items", [])
        if i.get("date")
    )
    first, last = (known[0], known[-1]) if known else (None, None)

    def explained(row: dict[str, Any]) -> bool:
        if row["id"] in cited or audit["id"] in cited:
            return True
        # a member counts as explained only where a statement cites it and names it (its ID or
        # its date), not where it is merely among a long citation list
        days = {i["id"]: str(i.get("date") or "") for i in row.get("items", []) if i.get("id")}
        for st in statements:
            text = st.get("text", "")
            said = {d.isoformat() for d in find_dates(text, first, last)}
            for m in set(row["members"]) & set(st.get("cites", [])):
                if m in text or (days.get(m) and days[m] in said):
                    return True
        return False

    return [
        f"{COVERAGE_ISSUE}{row['kind']} ({', '.join(row['members'][:4])})"
        for row in audit["rows"]
        if not explained(row)
    ]


# --- plain language: the record's internal vocabulary stays out of the prose -------------------

INTERNAL_ID = re.compile(
    r"\b(?:OI-\d+|F-[0-9a-f]{6,}|O-[0-9a-f]{6,}|R\d+(?:\.\d+)?|FIN:\S+|M:[A-Z]\S*)\b"
)
SNAKE = re.compile(r"\b[a-z]+(?:_[a-z0-9]+)+\b")
INTERNAL_PHRASES = re.compile(
    r"\b(?:open items?|fact fields?|fact ids?|(?:documented|corroborated|established|conflicting)"
    r" status|evidence kind|status claim|count audit|query results?)\b",
    re.I,
)


def jargon(answer: dict[str, Any], record: Record) -> list[str]:
    """The record's internal vocabulary in a statement: IDs, snake_case names, multi-word item
    kinds ("reading disagreement", "candidate link") and bookkeeping phrases. A style finding: it
    is repaired once and never withholds an answer."""
    kinds = {o.kind for o in record.open_items if "_" in o.kind}
    spaced = [re.compile(rf"\b{k.replace('_', '[ -]')}s?\b", re.I) for k in sorted(kinds)]
    found = []
    for i, st in enumerate(answer.get("statements", [])):
        text = st.get("text", "")
        terms = set(INTERNAL_ID.findall(text)) | set(SNAKE.findall(text))
        terms |= {m.group(0) for p in spaced + [INTERNAL_PHRASES] for m in p.finditer(text)}
        if terms:
            found.append(
                f"{STYLE_ISSUE}statement {i} uses the record's internal terms "
                f"({', '.join(sorted(terms)[:6])}); say what they mean in plain clinical words"
            )
    return found


# --- evidence given to the writer ------------------------------------------------------------


CONTEXT_CHARS = 120_000  # the record around a question, in priority order until spent


def question_scope(question: str, record: Record) -> tuple[list[str], set[str]]:
    """Events and dates a question names: its IDs, the events on its dates, the administrations
    of instruments it names."""
    low = question.lower()
    days = sorted(str(f.value)[:10] for f in record.facts if f.field == "date" and f.value)
    dates: set[str] = set()
    if days:
        first, last = date.fromisoformat(days[0]), date.fromisoformat(days[-1])
        dates = {d.isoformat() for d in find_dates(question, first, last)}
    kinds = {"encounter", "measurement", "medication", "charge", "goal"}
    events: list[str] = []
    for e in record.events:
        if e.kind not in kinds:
            continue
        facts = record.facts_of(e.id)
        instrument = str(facts["instrument"].value).lower() if facts.get("instrument") else ""
        if (
            re.search(rf"\b{re.escape(e.id.lower())}\b", low)
            or (_event_day(facts) in dates)
            or (instrument and instrument in low)
            or (e.kind == "goal" and re.search(r"\b(?:goals?|thresholds?|plans?)\b", low))
        ):
            events.append(e.id)
    return events, dates


def record_context(
    results: list[dict[str, Any]],
    record: Record,
    question: str = "",
    budget: int = CONTEXT_CHARS,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """The record around a question, not only the query results: every fact of the events the
    question names (by ID, date or instrument) and of the events in the results, the findings on
    the question's dates and in those events, and the open items that touch them. Numbers still
    bind only to cited results and facts, so the calculation guarantees do not change."""
    named, dates = question_scope(question, record)
    in_results: list[str] = []
    fact_subject = {f.id: f.subject for f in record.facts}
    for r in results:
        for row in list(r["rows"]) + list(r["excluded"]):
            for m in row.get("members", []) or []:
                in_results.append(m)
            for fid in row.get("facts", []) or []:
                if fid in fact_subject:
                    in_results.append(fact_subject[fid])
    order = list(dict.fromkeys(named + in_results))
    kinds = {e.id: e.kind for e in record.events}
    findings = [
        e.id
        for e in record.events
        if e.kind == "finding"
        and e.id not in order
        and (
            _event_day(record.facts_of(e.id)) in dates
            or (
                record.facts_of(e.id).get("encounter_id")
                and str(record.facts_of(e.id)["encounter_id"].value) in named
            )
        )
    ]
    order += findings
    by_subject: dict[str, list[Any]] = {}
    for f in record.facts:
        by_subject.setdefault(f.subject, []).append(f)
    facts: list[dict[str, Any]] = []
    used = 0
    for subject in order:
        for f in by_subject.get(subject, []):
            if kinds.get(subject) == "document":
                continue
            item = {
                "id": f.id,
                "subject": f.subject,
                "field": f.field,
                "value": f.value if f.status != "conflicting" else {"scenarios": f.scenarios},
                "status": f.status,
                "reason": f.reason[:160],
                "quotes": [
                    e.quote[:180]
                    for e in f.evidence
                    if e.stance in {"supports", "contradicts", "superseded"}
                ][:2],
            }
            size = len(json.dumps(item, default=str))
            if used + size > budget:
                break
            facts.append(item)
            used += size
    subjects = set(order)
    open_items = [
        {"id": f"OI-{n}", "kind": o.kind, "subject": o.subject, "text": o.text[:300]}
        for n, o in enumerate(record.open_items)
        if o.subject in subjects or any(fact_subject.get(x, x) in subjects for x in (o.facts or []))
    ]
    return facts, open_items


def compact_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for r in results:
        out.append(
            {
                "id": r["id"],
                "purpose": r.get("purpose"),
                "population": r.get("population"),
                "query": r["query"],
                "rows": [{k: v for k, v in row.items() if k != "facts"} for row in r["rows"]],
                "excluded_by_filter": [
                    {k: v for k, v in e.items() if k != "facts"} for e in r["excluded"]
                ][:40],
                "scenarios_are_range_endpoints": r["scenarios_are_range_endpoints"],
            }
        )
    return out


# --- ⑨ code checks ---------------------------------------------------------------------------


def _numbers(value: Any) -> set[float]:
    found: set[float] = set()
    if isinstance(value, bool):
        return found
    if isinstance(value, (int, float)):
        found.add(round(float(value), 2))
    elif isinstance(value, str):
        if not re.match(r"^\d{4}-\d{2}-\d{2}", value):
            found |= {round(float(n), 2) for n in NUMBER.findall(value)}
    elif isinstance(value, dict):
        for v in value.values():
            found |= _numbers(v)
    elif isinstance(value, list):
        for v in value:
            found |= _numbers(v)
    return found


def _times(value: Any) -> set[str]:
    # ensure_ascii=False keeps "09:00–09:50" intact; an escaped dash would hide the end time
    text = value if isinstance(value, str) else json.dumps(value, default=str, ensure_ascii=False)
    return {t for m in TIME.finditer(text) if (t := parse_time(m.group(0)))}


def day_counts(text: str) -> set[float]:
    """Numbers the text states as a number of days ("7 days", "seven days", "25 calendar days")."""
    found = set()
    words = [
        m.group(1)
        for pattern in (r"\b([\w-]+)[ -]days?\b", r"\b([\w-]+) \w+ days?\b")
        for m in re.finditer(pattern, text, re.I)
    ]
    for word in words:
        if (value := _count_value(word)) is not None:
            found.add(value)
    return found


def _with_hours(numbers: set[float]) -> set[float]:
    extra = set()
    for n in numbers:
        if n >= 60:
            extra |= {float(int(n // 60)), float(n % 60), round(n / 60, 2), round(n / 60, 1)}
    return numbers | extra


DATE_LIST = re.compile(
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s*\d{1,2}(?:st|nd|rd|th)?"
    r"(?:\s*(?:,\s*(?:and|or)?|and|&|or|–|-|→|to|through)\s*\d{1,2}(?:st|nd|rd|th)?\b(?![:.]\d))+",
    re.I,
)
UNIT_CONSTANTS = {60.0}  # minutes per hour, used in conversions
_UNITS = "one two three four five six seven eight nine".split()
_TEENS = "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "twenty thirty forty fifty sixty seventy eighty ninety".split()
WORD_VALUES = (
    {w: n for n, w in enumerate(_UNITS, start=1)}
    | {w: n for n, w in enumerate(_TEENS, start=10)}
    | {w: 20 + 10 * n for n, w in enumerate(_TENS)}
)
NUMBER_WORD = re.compile(
    rf"\b({'|'.join(_UNITS[3:] + _TEENS + _TENS)})(?:-({'|'.join(_UNITS)}))?\b", re.I
)
MONTH_NAME = re.compile(
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s*\d", re.I
)
ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def stated(text: str, names: list[str]) -> tuple[set[float], set[str]]:
    """Numbers and times a statement asserts, excluding dates, record IDs/names and ordinals."""
    spans = date_spans(text) + [m.span() for m in DATE_LIST.finditer(text)]
    for name in names:
        spans += [m.span() for m in re.finditer(re.escape(name), text, re.I)]
    cleaned = text
    for s, e in sorted(set(spans), reverse=True):
        cleaned = cleaned[:s] + " " + cleaned[e:]
    cleaned = re.sub(
        r"\b(?:week|item|goal|session|scenario|visit|day|question|example|step|part|point|"
        r"option|case|record|pair|group|note|instance|finding|issue|reason)s?\s*#?\d+"
        r"(?:\s*(?:,\s*(?:and|or)?|and|or|&|–|-|to|through)\s*\d+)*\b",
        " ",
        cleaned,
        flags=re.I,
    )
    # list markers, including a range of items ("(1)", "(2–4)", "3.")
    cleaned = re.sub(r"\(\d{1,2}(?:\s*[–-]\s*\d{1,2})?\)|(?:^|\s)\d{1,2}[.)](?=\s)", " ", cleaned)
    # a label heading a sentence ("Instance 2 —", "Week 3:") numbers the list, not a value
    cleaned = re.sub(r"(?:^|(?<=[.;]\s))[A-Z][a-z]+ \d{1,2}\s*(?:—|–|:|\))", " ", cleaned)
    cleaned = re.sub(r"\b[A-Za-z]+-\d+\b", " ", cleaned)
    times = {t for m in TIME.finditer(cleaned) if (t := parse_time(m.group(0)))}
    cleaned = TIME.sub(" ", cleaned)
    if MONTH_NAME.search(text):
        cleaned = re.sub(r"\b(?:19|20)\d{2}\b", " ", cleaned)  # a year beside a date
    numbers = {round(float(n), 2) for n in NUMBER.findall(cleaned)}
    # a count written as a word is a number like any other; "one" to "three" are left out, as
    # often an article or a figure of speech ("the two notes", "three weeks") as a count
    for m in NUMBER_WORD.finditer(cleaned):
        numbers.add(
            float(WORD_VALUES[m.group(1).lower()] + WORD_VALUES.get((m.group(2) or "").lower(), 0))
        )
    return numbers, times


def _row_numbers(row: dict[str, Any]) -> set[float]:
    values = _numbers({k: v for k, v in row.items() if k not in {"id", "members", "facts"}})
    return _with_hours(values | {abs(x) for x in values})


def _arithmetic(n: float, values: set[float]) -> str | None:
    """A sum, difference or percentage of two cited values that equals n (verified by code)."""
    pool = sorted({v for v in values if v != 0}, reverse=True)[:120]
    for i, a in enumerate(pool):
        for j, b in enumerate(pool):
            if i == j:
                continue
            if abs(a + b - n) < 0.01:
                return f"{a:g} + {b:g}"
            if a > b and abs(a - b - n) < 0.01:
                return f"{a:g} − {b:g}"
            if b and abs(round(100 * a / b, 1) - n) < 0.051:
                return f"{a:g} / {b:g} × 100"
    return None


# a clause stating one scenario ("under the 40-minute scenario", "if the start was 09:10") presents
# a scenario on purpose, not a conflicting value as settled
CONDITIONAL = re.compile(
    r"\b(?:scenario|if|would|assuming|were it|had it|under the \w+(?:[ -]\w+)? rule)\b", re.I
)
COMBINED = re.compile(
    r"\b(?:totals?|combined|overall|altogether|in all|sums?|aggregate|reconcil\w*|across|"
    r"grand)\b",
    re.I,
)
# an item scoped to each group ("total minutes per week") asks for the group rows, not the total
# across groups, unless it also asks for the whole ("per week and overall")
PER_GROUP = re.compile(
    r"\b(?:per|each|every|by)\s+(?:week|service|day|date|month|type|visit|session)\b|\bweekly\b",
    re.I,
)
WHOLE = re.compile(r"\b(?:combined|overall|altogether|in all|across|grand)\b", re.I)
BALANCE = re.compile(
    r"\b(?:remain(?:s|ing)?|left over|leftover|balance|unused|still available|outstanding)\b", re.I
)


def _elapsed(n: float, times: set[str]) -> str | None:
    """n minutes between two cited clock times (13:20 to 13:30 is 10), verified by code."""
    minutes = sorted({int(t[:2]) * 60 + int(t[3:5]) for t in times if re.match(r"^\d{2}:\d{2}", t)})
    for i, a in enumerate(minutes):
        for b in minutes[i + 1 :]:
            if abs(b - a - n) < 0.01:
                return f"{b // 60:02d}:{b % 60:02d} − {a // 60:02d}:{a % 60:02d}"
    return None


# --- goal outcomes and weekdays stated in prose must match what code computed -----------------

OUTCOME_WORDS = (
    r"(?:not|never)(?: yet)?(?: been)? (?:met|achieved)|\w+n't(?: been)? (?:met|achieved)|"
    r"cannot be determined|could not be determined|cannot determine|"
    r"can't be determined|undetermined|indeterminate|met|achieved"
)
UNIT_WORDS = {"days": r"(?:therapy[- ])?days?", "minutes": r"minutes?", "sessions": r"sessions?"}


def _outcome(word: str) -> str:
    w = word.lower()
    if (w.startswith(("not ", "never ")) or "n't " in w) and not w.endswith("determined"):
        return "not_met"
    if w in {"met", "achieved"}:
        return "met"
    return "cannot_determine"


# words that turn "met" into "cannot say whether met" ("neither can be confirmed as met or not met")
UNDECIDED = re.compile(
    r"\b(?:neither|nor|cannot|can't|could not|couldn't|unable|whether|unclear|unknown|"
    r"not be (?:confirmed|determined|judged|assessed|established))\b",
    re.I,
)
EITHER_WAY = re.compile(r"\s*(?:or|nor)\s+(?:not\s+)?(?:met|achieved)\b", re.I)


def goal_claims(text: str) -> dict[str, set[str]]:
    """Outcomes a sentence states per goal unit ("the days goal was met; the minutes goal cannot
    be determined")."""
    found: dict[str, set[str]] = defaultdict(set)
    for unit, words in UNIT_WORDS.items():
        pattern = rf"\b{words}\s+(?:goal|target|threshold|requirement|criterion)\b[^.;]{{0,80}}?\b({OUTCOME_WORDS})\b"
        for m in re.finditer(pattern, text, re.I):
            outcome = _outcome(m.group(1))
            if UNDECIDED.search(m.group(0)) or EITHER_WAY.match(text, m.end()):
                outcome = "cannot_determine"
            found[unit].add(outcome)
    return found


# a claim about the goal as a whole ("the patient did not meet the weekly therapy goal")
OVERALL_CLAIMS = [
    re.compile(
        r"\b(did not meet|didn't meet|does not meet|doesn't meet|failed to meet|did meet|met|meets)"
        r"\s+(?:(?:the|his|her|their|its|this|that|each|every)\s+)?(?:[\w-]+\s+){0,3}goals?\b",
        re.I,
    ),
    re.compile(
        r"\bgoals?\s+(?:was|were|is|are|has been|have been)\s+(not\s+)?(?:met|achieved)\b", re.I
    ),
]


def overall_claims(text: str) -> set[str]:
    """met / not_met claimed about the goal as a whole; "whether the goal was met" is no claim."""
    found = set()
    for n, pattern in enumerate(OVERALL_CLAIMS):
        for m in pattern.finditer(text):
            # the clause before the claim ("... to determine whether the composite goal was met")
            before = re.split(r"[,:;—]", text[max(0, m.start() - 60) : m.start()])[-1]
            if UNDECIDED.search(before) or UNDECIDED.search(m.group(0)):
                continue
            if EITHER_WAY.match(text, m.end()):
                continue
            word = m.group(1) or ""
            negative = bool(re.search(r"not|n't|failed", word)) if n == 0 else bool(word)
            found.add("not_met" if negative else "met")
    return found


# a clause about several weeks at once ("the other three weeks", "every week") is not a claim
# about one week's result
SEVERAL_WEEKS = re.compile(
    r"\b(?:weeks|each week|every week|any week|all\s+(?:\w+\s+)?weeks?)\b", re.I
)


def goal_outcome_issues(
    i: int, text: str, cited: list[dict[str, Any]], first: date | None, last: date | None
) -> list[str]:
    """A statement's per-threshold goal outcomes must equal the goal_met() checks it cites. Each
    clause is checked against the week it names; a clause naming no week refers to the week the
    statement names, and a clause about several weeks is not checked against any one week."""
    # a sentence explaining one scenario ("under the 50-minute scenario the goal is met") is not a
    # claim about the week as a whole
    conditional = re.compile(r"\b(?:scenario|if|under|would|either|whichever)\b", re.I)
    goal_rows = [r for r in cited if isinstance(r.get("goal_met()"), dict)]
    # with no documented goal there is nothing to meet or miss, whichever week is meant
    if goal_rows and all(r["goal_met()"].get("status") == "no_goal" for r in goal_rows):
        said: set[str] = set()
        for sentence in re.split(r"(?<=[.])\s+", text):
            per_unit = goal_claims(sentence)
            said |= {o for v in per_unit.values() for o in v}
            if not per_unit and not conditional.search(sentence):
                said |= overall_claims(sentence)
        if said & {"met", "not_met"}:
            return [
                f"statement {i}: says the goal was {'/'.join(sorted(said & {'met', 'not_met'})).replace('_', ' ')}, "
                "but no documented goal applies (goal_met() = no_goal); say the goal cannot be "
                "judged because no care goal is documented"
            ]
        return []
    # the same week cited through several results is one week
    unique: dict[str, dict[str, Any]] = {}
    for r in goal_rows:
        unique.setdefault(str(r.get("covered") or r.get("group") or r.get("id")), r)
    weeks = list(unique.values())

    def span(r: dict[str, Any]) -> str:
        return str(r.get("covered") or r.get("group") or "")

    def named(part: str) -> list[dict[str, Any]]:
        days = find_dates(part, first, last)
        return [
            r for r in weeks if any(span(r)[:10] <= d.isoformat() <= span(r)[-10:] for d in days)
        ]

    whole = named(text) if len(weeks) > 1 else weeks
    # claims per week (keyed by the row's position): stated, hedged by a scenario, about the whole goal
    claims: dict[int, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    hedged: dict[int, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    overall: dict[int, set[str]] = defaultdict(set)
    for sentence in re.split(r"(?<=[.])\s+", text):
        clauses: list[str] = []
        for part in re.split(r";\s*", sentence):
            # a lead-in naming no week before a colon is a summary, not the heading of a week
            head, colon, rest = part.partition(": ")
            dated_head = find_dates(head, first, last) or not colon
            clauses += [part] if dated_head else [head, rest]
        for clause in clauses:
            per_unit = goal_claims(clause)
            is_hedged = bool(conditional.search(sentence))
            said_overall = overall_claims(clause) if not per_unit and not is_hedged else set()
            if not per_unit and not said_overall:
                continue
            if find_dates(clause, first, last):
                target = named(clause)
            elif SEVERAL_WEEKS.search(clause):
                continue
            else:
                target = whole
            if len(target) != 1:
                continue
            k = weeks.index(target[0])
            for unit, said in per_unit.items():
                (hedged if is_hedged else claims)[k][unit] |= said
            overall[k] |= said_overall
    issues = []
    for k, row in enumerate(weeks):
        if not (claims.get(k) or hedged.get(k) or overall.get(k)):
            continue
        computed: dict[str, set[str]] = defaultdict(set)
        for check in row["goal_met()"].get("checks", []):
            if check.get("outcome") != "not_applicable":
                computed[check["unit"]].add(check["outcome"])
        status = row["goal_met()"].get("status")
        week = f" ({span(row).replace('..', ' to ')})" if len(weeks) > 1 else ""
        said_overall = overall.get(k, set())
        if (
            said_overall
            and status in {"met", "not_met", "cannot_determine"}
            and not said_overall <= {status}
        ):
            issues.append(
                f"statement {i}: says the goal was {'/'.join(sorted(said_overall)).replace('_', ' ')}, but "
                f"the computed result for that week{week} is {status.replace('_', ' ')}"
            )
        stated_claims = claims[k]
        for unit, said in hedged.get(k, {}).items():
            # scenario-by-scenario outcomes are fine when the week as a whole cannot be determined
            if computed.get(unit) and not (
                said <= computed[unit]
                or (computed[unit] == {"cannot_determine"} and said <= {"met", "not_met"})
            ):
                stated_claims[unit] |= said
        for unit, said in stated_claims.items():
            if computed.get(unit) and not said <= computed[unit]:
                issues.append(
                    f"statement {i}: says the {unit} goal is {'/'.join(sorted(said)).replace('_', ' ')}, "
                    f"but the computed result for that week{week} is {'/'.join(sorted(computed[unit])).replace('_', ' ')} "
                    f"(per threshold: "
                    + ", ".join(
                        f"{u} {'/'.join(sorted(o)).replace('_', ' ')}"
                        for u, o in sorted(computed.items())
                    )
                    + ")"
                )
    return issues


# a count followed within three words by a plural noun ("six encounters", "two counted sessions")
COUNT_PHRASE = re.compile(
    r"(?<![\w-])(\d+|[A-Za-z]+(?:-[a-z]+)?)\s+(?:[a-z-]+\s+){0,2}[a-z-]{3,}(?<!ss)s\b"
)
MONTH_BEFORE = re.compile(
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s*$", re.I
)


def _count_value(word: str) -> float | None:
    if word.isdigit():
        return float(word)
    head, _, tail = word.lower().partition("-")
    if head in WORD_VALUES:
        return float(WORD_VALUES[head] + WORD_VALUES.get(tail, 0))
    return None


def _top_level_items(text: str) -> list[str]:
    """A list's items split at commas and "and" outside brackets."""
    items, depth, current = [], 0, ""
    for ch in text:
        depth += ch in "([" and 1 or 0
        depth -= ch in ")]" and 1 or 0
        if ch == "," and depth == 0:
            items.append(current)
            current = ""
        else:
            current += ch
    items.append(current)
    out = []
    for item in items:
        out += [x for x in re.split(r"\s+and\s+(?![^()]*\))", item.strip()) if x.strip()]
    return [re.sub(r"^and\s+", "", x.strip()) for x in out if x.strip() and x.strip() != "and"]


def list_count_issues(i: int, text: str, item_ids: set[str]) -> list[str]:
    """A count that introduces a list ("Six visits were not counted: A (V1), B (V2), ...") must
    equal the number of items listed. Checked only when every listed item names its own record,
    so the list's items are known without reading its wording."""
    issues = []
    for sentence in re.split(r"(?<=[.])\s+", text):
        head, colon, listed = sentence.partition(":")
        if not colon:
            continue
        # the last count before the colon introduces the list; a day of a date is no count
        counts = [
            m
            for m in COUNT_PHRASE.finditer(head)
            if _count_value(m.group(1)) is not None and not MONTH_BEFORE.search(head[: m.start()])
        ]
        if not counts:
            continue
        word = counts[-1].group(1)
        n = _count_value(word)
        items = _top_level_items(listed.strip().rstrip("."))
        named = [
            {x for x in item_ids if re.search(rf"(?<![\w-]){re.escape(x)}(?![\w-])", item)}
            for item in items
        ]
        if len(items) >= 2 and all(len(ids) == 1 for ids in named) and len(items) != n:
            issues.append(
                f"statement {i}: says {word} but lists {len(items)} "
                f"({', '.join(sorted(set().union(*named)))}); state the number listed"
            )
    return issues


WEEKDAY = r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
MONTH_DAY = r"(\d{4}-\d{2}-\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}(?:,\s*\d{4})?)"
WEEKDAY_PAIRS = [
    re.compile(rf"\b{WEEKDAY},?\s+{MONTH_DAY}", re.I),
    re.compile(
        rf"\b{MONTH_DAY}\s*(?:\(|,\s*|\s+(?:is|was|falls on|fell on)\s+(?:an?\s+)?){WEEKDAY}\b",
        re.I,
    ),
]


def weekday_issues(i: int, text: str, first: date | None, last: date | None) -> list[str]:
    """A weekday written next to a date must be that date's weekday (computed, never guessed)."""
    issues = []
    for n, pattern in enumerate(WEEKDAY_PAIRS):
        for m in pattern.finditer(text):
            name, when = (m.group(1), m.group(2)) if n == 0 else (m.group(2), m.group(1))
            days = find_dates(when, first, last)
            if len(days) != 1:
                continue
            day = next(iter(days))
            actual = day.strftime("%A")
            if actual.lower() != name.lower():
                issues.append(
                    f"statement {i}: {when.strip()} is a {actual}, not a {name}; use the weekday "
                    "column of the results"
                )
    return issues


def code_check(
    answer: dict[str, Any],
    results: list[dict[str, Any]],
    record: Record,
    passages: dict[str, str] | None = None,
    question: str = "",
    index: PassageIndex | None = None,
    required_totals: list[dict[str, Any]] | None = None,
) -> tuple[list[str], list[str]]:
    """(blocking issues, results to attach in full).

    Binding: every number and time must be a value of the statement's cited rows, facts or
    passages. When it is not, code repairs what it can prove: a number held by exactly one result
    row (or a large number held by any) gets that row added to the citations, and a sum,
    difference or percentage of two cited values is accepted with the arithmetic recorded.
    Dates in a narrative statement must be dates of its cited evidence."""
    passages = passages or {}
    issues: list[str] = []
    # numbers the question itself states (a premise being checked, "55 minutes") may be repeated
    asked = stated(question, [])[0] if question else set()
    rows = {row["id"]: row for r in results for row in r["rows"]}
    whole = {
        r["id"]: {
            "rows": [
                {k: v for k, v in row.items() if k not in {"id", "members", "facts"}}
                for row in r["rows"]
            ]
        }
        for r in results
    }
    facts = {f.id: f for f in record.facts}
    by_event: dict[str, list[Any]] = {}
    for f in record.facts:
        by_event.setdefault(f.subject, []).append(f)
    open_ids = {f"OI-{n}": o for n, o in enumerate(record.open_items)}
    names = sorted(
        {e.id for e in record.events}
        | {str(f.value) for f in record.facts if f.field in {"instrument", "name"} and f.value},
        key=len,
        reverse=True,
    )
    days = sorted(str(f.value) for f in record.facts if f.field == "date" and f.value)
    first_day = date.fromisoformat(days[0][:10]) if days else None
    last_day = date.fromisoformat(days[-1][:10]) if days else None
    doc_days: dict[str, set[str]] = {}
    if index is not None and first_day and last_day:
        for bid, _name, text in index.blocks:
            doc_days.setdefault(bid.split(":", 1)[0], set()).update(
                d.isoformat() for d in find_dates(text, first_day, last_day)
            )
    for i, s in enumerate(answer.get("statements", [])):
        unknown = [
            c
            for c in s["cites"]
            if c not in rows
            and c not in facts
            and c not in whole
            and c not in by_event
            and c not in open_ids
            and c not in passages
        ]
        if unknown:
            # an unresolvable citation is removed; the statement must still bind to what remains
            s["cites"] = [c for c in s["cites"] if c not in unknown]
            s.setdefault("removed_cites", []).extend(unknown)
        if not s["cites"] and s["kind"] != "missing":
            issues.append(
                f"statement {i}: cites nothing that resolves"
                + (f" (unknown IDs {unknown})" if unknown else "")
            )
        allowed_n: set[float] = set()
        allowed_t: set[str] = set()
        computed: set[float] = set()  # values results and facts hold (the only arithmetic inputs)
        for c in s["cites"]:
            if c in rows:
                computed |= _numbers(
                    {k: v for k, v in rows[c].items() if k not in {"id", "members", "facts"}}
                )
                allowed_n |= _numbers(
                    {k: v for k, v in rows[c].items() if k not in {"id", "members", "facts"}}
                )
                allowed_t |= _times(rows[c])
            elif c in whole:
                allowed_n |= _numbers(whole[c])
                allowed_t |= _times(whole[c])
            for f in [facts[c]] if c in facts else by_event.get(c, []):
                computed |= _numbers(f.values())
                allowed_n |= _numbers(f.values())
                allowed_t |= _times(f.values()) | {t for e in f.evidence for t in _times(e.quote)}
                allowed_n |= {n for e in f.evidence for n in _numbers(e.quote)}
            if c in open_ids:
                allowed_n |= _numbers(open_ids[c].text)
                allowed_t |= _times(open_ids[c].text)
            if c in passages:
                allowed_n |= _numbers(passages[c])
                allowed_t |= _times(passages[c])
        # day numbers of dates in the cited evidence ("Jan 5, 6, 9 [...], 21")
        cited_dates: set[str] = set()
        for c in s["cites"]:
            source = rows.get(c) or whole.get(c)
            if source:
                cited_dates |= set(ISO_DATE.findall(json.dumps(source, default=str)))
                for m in (rows.get(c) or {}).get("members", []):
                    cited_dates |= {
                        str(f.value) for f in by_event.get(m, []) if f.field == "date" and f.value
                    }
            for f in by_event.get(c, []) + ([facts[c]] if c in facts else []):
                if f.valid_time:
                    cited_dates.add(f.valid_time)
        allowed_n |= {float(d[8:10]) for d in cited_dates if len(d) >= 10}
        allowed_n |= {abs(n) for n in allowed_n} | UNIT_CONSTANTS | asked
        # a count of the items the statement itself cites is verifiable by code
        cited_items = [c for c in s["cites"] if c in by_event]
        members = {m for c in s["cites"] if c in rows for m in rows[c].get("members", [])}
        allowed_n |= {float(len(cited_items)), float(len(members))}
        # counts of the statement's own citations by kind (four conflicts cited: "four conflicts")
        by_kind = Counter(
            "open"
            if c in open_ids
            else "fact"
            if c in facts
            else "passage"
            if c in passages
            else "row"
            if c in rows
            else "item"
            for c in s["cites"]
        )
        allowed_n |= {float(n) for n in by_kind.values()}
        # the number of groups the statement cites ("four weeks" citing each week's row)
        allowed_n.add(
            float(
                len(
                    {
                        str(rows[c].get("group"))
                        for c in s["cites"]
                        if c in rows and rows[c].get("group") not in (None, "all")
                    }
                )
            )
        )
        # a number of days between dates the statement or its evidence names ("received seven
        # days later", "the seven days of Jan 26–Feb 1"), only where the text says days
        named_days = sorted(
            {date.fromisoformat(d[:10]) for d in cited_dates if len(d) >= 10}
            | set(find_dates(s["text"], first_day, last_day) if first_day else [])
        )
        spans = {
            float((b - a).days + inclusive)
            for i, a in enumerate(named_days)
            for b in named_days[i + 1 :]
            for inclusive in (0, 1)
        }
        allowed_n |= spans & day_counts(s["text"])
        numbers, times = stated(s["text"], names)
        missing_n = sorted(numbers - _with_hours(allowed_n))
        missing_t = sorted(times - allowed_t)
        if missing_t:
            # a time held by a fact of a record the statement cites or names is bound to that
            # fact: code adds the citation (as for numbers held by one result row)
            about = {m for c in s["cites"] if c in rows for m in rows[c].get("members", [])}
            about |= {c for c in s["cites"] if c in by_event}
            about |= {e for e in by_event if len(e) > 3 and e in s["text"]}
            for t in list(missing_t):
                holder = next(
                    (
                        f
                        for e in sorted(about)
                        for f in by_event.get(e, [])
                        if t
                        in _times(f.values()) | {x for ev in f.evidence for x in _times(ev.quote)}
                    ),
                    None,
                )
                if holder is not None:
                    s["cites"].append(holder.id)
                    s.setdefault("added_cites", []).append(holder.id)
                    missing_t.remove(t)
        unresolved = []
        for n in missing_n:
            holders = [rid for rid, row in rows.items() if n in _row_numbers(row)]
            if len(holders) == 1 or (holders and n >= 10):
                s["cites"].append(holders[0])  # code-proven citation
                s.setdefault("added_cites", []).append(holders[0])
                allowed_n |= _row_numbers(rows[holders[0]])
                computed |= _numbers(
                    {
                        k: v
                        for k, v in rows[holders[0]].items()
                        if k not in {"id", "members", "facts"}
                    }
                )
                continue
            unresolved.append(n)
        for n in list(unresolved):
            proof = _arithmetic(n, {abs(x) for x in computed}) or _elapsed(n, allowed_t)
            if proof and BALANCE.search(s["text"]):
                # a remaining balance is a conclusion about what is left, not arithmetic on two
                # cited values: only a computed result may state it
                issues.append(
                    f"statement {i}: {n:g} is a remaining balance worked out from cited values "
                    f"({proof}); no computed result states it, so say what the record documents "
                    f"(the authorized and used quantities) without a balance"
                )
                unresolved.remove(n)
                continue
            if proof:
                s.setdefault("verified_arithmetic", []).append(f"{n:g} = {proof}")
                unresolved.remove(n)
        if unresolved:
            issues.append(
                f"statement {i}: {', '.join(f'{n:g}' for n in unresolved)} is in no cited result, "
                f"fact or passage and is not a sum, difference, percentage or elapsed time of cited "
                f"values; cite "
                f"the result that states it or remove it"
            )
        # dates in a narrative statement must belong to its evidence (no reason moved to a
        # different day)
        if s["kind"] == "narrative" and first_day:
            evidence_days = set(cited_dates)
            for c in s["cites"]:
                if c in passages:
                    evidence_days |= {
                        d.isoformat() for d in find_dates(passages[c], first_day, last_day)
                    }
                for f in [facts[c]] if c in facts else by_event.get(c, []):
                    evidence_days |= {
                        d.isoformat()
                        for e in f.evidence
                        for d in find_dates(e.quote, first_day, last_day)
                    }
                    # a statement about the evidence's documents may give those documents' own
                    # dates (received, signed, corrected), not dates from elsewhere in the record
                    for e in f.evidence:
                        evidence_days |= doc_days.get(e.block.split(":", 1)[0], set())
                if c in passages:
                    evidence_days |= doc_days.get(c.split(":", 1)[0], set())
            # a range the statement names ("January 12-18") is bound by its endpoints
            said = {d.isoformat() for d in find_dates(s["text"], first_day, last_day, expand=False)}
            stray = sorted(said - evidence_days)
            if stray and evidence_days:
                issues.append(
                    f"statement {i}: date {', '.join(stray)} is not a date of its cited evidence "
                    f"({', '.join(sorted(evidence_days)[:6])}); cite the evidence for that date, or "
                    f"attach each fact to its own date"
                )
        if missing_t:
            issues.append(f"statement {i}: time {', '.join(missing_t)} is not in its cited facts")
        for c in s["cites"]:
            cited_fact = facts.get(c)
            about_event = c in by_event and (
                c.lower() in s["text"].lower() or len([x for x in s["cites"] if x in by_event]) == 1
            )
            # only a plain value or narrative can present a conflict as settled; a conflict,
            # inference ("at least 40") or missing statement is about the conflict itself
            candidates = (
                []
                if s["kind"] not in {"value", "narrative"} or CONDITIONAL.search(s["text"])
                else [cited_fact]
                if cited_fact
                else [x for x in by_event.get(c, []) if x.status == "conflicting"]
                if about_event
                else []
            )
            for f in candidates:
                if f.status != "conflicting":
                    continue
                numeric = [round(float(v), 2) for v in f.scenarios if isinstance(v, (int, float))]
                clocks = [
                    parse_time(v) for v in f.scenarios if isinstance(v, str) and parse_time(v)
                ]
                shown = _with_hours(numbers)
                # stating some scenarios but not all presents a conflict as settled
                partial_n = numeric and (set(numeric) & shown) and not set(numeric) <= shown
                partial_t = clocks and (set(clocks) & times) and not set(clocks) <= times
                if partial_n or partial_t:
                    issues.append(
                        f"statement {i}: {f.subject} {f.field} is conflicting "
                        f"({' or '.join(map(str, f.scenarios))}); state every scenario"
                    )
            direct = facts.get(c)
            if direct and direct.status == "not_documented" and s["kind"] == "value":
                issues.append(
                    f"statement {i}: asserts {direct.subject} {direct.field}, which is not documented"
                )
    # each checklist item the planner marked as a combined figure must be stated from the result
    # that computes it (a grouped result's "all groups" row, or an ungrouped result)
    cited = set()
    for s in answer.get("statements", []):
        for c in s["cites"]:
            cited.add(c)
            cited.add(c.rsplit(".", 1)[0])  # a row cites its result too
    stated_numbers = {n for s in answer.get("statements", []) for n in stated(s["text"], [])[0]}
    by_id = {r["id"]: r for r in results}
    for need in required_totals or []:
        item = str(need.get("item", "")) if isinstance(need, dict) else ""
        if not COMBINED.search(item) or (PER_GROUP.search(item) and not WHOLE.search(item)):
            continue  # the planner may mark a per-week list; only a combined figure is required
        r = by_id.get(f"R{need.get('query')}")
        if r is None or not r["rows"]:
            continue
        total_rows = [x for x in r["rows"] if str(x["id"]).endswith(".all")] or (
            r["rows"] if len(r["rows"]) == 1 else []
        )
        # an item about one group ("total minutes in the week of January 19-25") is that group's
        # row, not the total across groups
        named = find_dates(str(need.get("item", "")), expand=False)
        covering = [
            x
            for x in r["rows"]
            if ".." in str(x.get("group", ""))
            and named
            and all(str(x["group"])[:10] <= d.isoformat() <= str(x["group"])[-10:] for d in named)
        ]
        if covering:
            total_rows = covering[:1]
        if not total_rows:
            continue
        trow = total_rows[0]
        values = _numbers({k: v for k, v in trow.items() if k not in {"id", "members", "facts"}})
        if not values:
            continue  # nothing combined to state
        if trow["id"] in cited or (r["id"] in cited and values & stated_numbers):
            continue
        summary = ", ".join(
            f"{k} = {v}"
            for k, v in trow.items()
            if k not in {"id", "group", "members", "facts"} and not isinstance(v, list)
        )
        issues.append(
            f'checklist item "{need.get("item", "")}" needs the combined figure: state it from '
            f"{trow['id']} ({summary}) and cite {trow['id']}"
        )
    # completeness: listed results must be enumerated, or they are attached in full
    attach = []
    text = " ".join(s["text"] for s in answer.get("statements", []))
    for r in results:
        for row in r["rows"]:
            listed = next(
                (
                    v
                    for k, v in row.items()
                    if k.startswith(("list(", "rows(")) and isinstance(v, list)
                ),
                None,
            )
            if not listed:
                continue
            absent = [
                item
                for item in listed
                if not any(
                    str(item.get(key, "")) and _mentioned(str(item.get(key)), text)
                    for key in ("id", "date", "text")
                )
            ]
            if absent:
                attach.append(r["id"])
    for i, s in enumerate(answer.get("statements", [])):
        cited_rows = [rows[c] for c in s.get("cites", []) if c in rows]
        cited_rows += [
            row for c in s.get("cites", []) if c in whole for row in _result_rows(results, c)
        ]
        issues += goal_outcome_issues(i, s["text"], cited_rows, first_day, last_day)
        issues += weekday_issues(i, s["text"], first_day, last_day)
        issues += list_count_issues(i, s["text"], set(by_event))
    return issues, sorted(set(attach))


def _mentioned(value: str, text: str) -> bool:
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        day = date.fromisoformat(value)
        return day in find_dates(text, day, day)
    return value.lower()[:40] in text.lower()


EVIDENCE_CHARS = 24000  # per statement; the check sees the most specific evidence first


def _cap(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep a statement's evidence within budget: whole results cited as a block can be huge, so
    items are kept in citation order until the budget is spent, and the cut is said openly."""
    kept: list[dict[str, Any]] = []
    used = 0
    for item in evidence:
        size = len(json.dumps(item, default=str))
        if used + size > EVIDENCE_CHARS:
            text = json.dumps(item, default=str)[: max(0, EVIDENCE_CHARS - used)]
            if text:
                kept.append({"truncated": text})
            kept.append({"note": f"{len(evidence) - len(kept)} more cited items not shown"})
            break
        kept.append(item)
        used += size
    return kept


def is_aggregate(result: dict[str, Any]) -> bool:
    """A result that counts, sums or averages (its rows hold aggregate columns)."""
    if result.get("purpose") == AUDIT_PURPOSE:
        return False
    return any(
        k.startswith(("count(", "count_distinct(", "sum(", "avg(", "min(", "max("))
        for row in result.get("rows", [])
        for k in row
    )


def model_check(
    question: str,
    plan: dict[str, Any],
    answer: dict[str, Any],
    results: list[dict[str, Any]],
    record: Record,
    passages: dict[str, str] | None = None,
    index: PassageIndex | None = None,
) -> tuple[list[str], dict[str, Any]]:
    passages = passages or {}
    rows = {row["id"]: row for r in results for row in r["rows"]}
    facts = {f.id: f for f in record.facts}
    open_ids = {f"OI-{n}": o for n, o in enumerate(record.open_items)}
    statements = []
    for i, s in enumerate(answer.get("statements", [])):
        evidence: list[dict[str, Any]] = []
        for c in s["cites"]:
            if c in open_ids:
                o = open_ids[c]
                evidence.append({"open_item": {"id": c, "kind": o.kind, "text": o.text}})
            elif c in facts:
                f = facts[c]
                evidence.append(
                    {
                        "fact": f"{f.subject} {f.field} = {f.values()}",
                        "quotes": [e.quote for e in f.evidence][:3],
                    }
                )
            elif c in passages:
                evidence.append({"passage": passages[c]})
            elif c in rows:
                evidence.append(
                    {"result": {k: v for k, v in rows[c].items() if k not in {"facts"}}}
                )
            elif c.startswith("R") and any(r["id"] == c for r in results):
                evidence.append(
                    {
                        "result": [
                            {k: v for k, v in row.items() if k != "facts"}
                            for r in results
                            if r["id"] == c
                            for row in r["rows"]
                        ]
                    }
                )
            else:
                for f in [x for x in record.facts if x.subject == c][:12]:
                    evidence.append(
                        {
                            "fact": f"{f.subject} {f.field} = {f.values()}",
                            "quotes": [e.quote for e in f.evidence][:2],
                        }
                    )
        if index is not None:
            # the full source lines behind the cited facts: a quote alone can hide what the rest
            # of the line says ("No correction sheet was included")
            cited = {c for c in s["cites"]}
            lines: list[str] = []
            for f in record.facts:
                if f.id in cited or f.subject in cited:
                    lines += [e.block for e in f.evidence if e.block not in lines]
            evidence += [
                {"source_line": b, "text": text}
                for b in lines[:16]
                if b not in passages and (text := index.text(b))
            ]
        statements.append(
            {"index": i, "kind": s["kind"], "text": s["text"], "evidence": _cap(evidence)}
        )
    payload = json.dumps(
        {
            "question": question,
            "checklist": plan.get("checklist", []),
            "results": [
                {
                    "result": r["id"],
                    "query": r["query"],
                    "population": r.get("population", ""),
                    "counted": r.get("counted", ""),
                }
                # only results that count or add something up have a population to judge;
                # listings, open items and the list of records a count left out are context
                for r in results
                if is_aggregate(r)
            ],
            "statements": statements,
        },
        default=str,
    )
    verdict = llm.call("check", CHECK, payload, CHECK_SCHEMA, llm.SMALL, 12000)
    # lists the model serialized as text are parsed, never read character by character
    verdict = {
        **verdict,
        **{
            k: llm.as_list(verdict.get(k))
            for k in ("question_parts", "checklist", "populations", "statements")
        },
    }
    issues = [
        f"{PART_ISSUE}{c['part']}"
        for c in verdict.get("question_parts", [])
        if not c.get("addressed")
    ]
    issues += [
        f"{CHECKLIST_ISSUE}{c['item']}"
        for c in verdict.get("checklist", [])
        if not c.get("addressed")
    ]
    issues += [
        f"{POPULATION_ISSUE}{p.get('result')}: {p.get('why', '')[:200]}"
        for p in verdict.get("populations", [])
        if isinstance(p, dict) and p.get("matches") is False
    ]
    kinds = {i: s["kind"] for i, s in enumerate(answer.get("statements", []))}
    issues += [
        f"statement {v['index']}: not supported by its cited evidence ({v.get('why', '')[:160]})"
        for v in verdict.get("statements", [])
        if not v.get("supported")
        and kinds.get(v["index"]) in {"narrative", "inference", "value", "missing"}
    ]
    return issues, verdict


def listed_entries(row: dict[str, Any], record: Record) -> list[dict[str, Any]]:
    """A result row, the items shown inside it, and the records it counts or lists (its members)
    with the documents that support each and their role: whatever columns the query selected, a
    copy or a correction behind a counted item is visible."""
    entries = [row] + [
        x for v in row.values() if isinstance(v, list) for x in v if isinstance(x, dict)
    ]
    shown = {str(e.get("id")) for e in entries}
    for member in row.get("members") or []:
        if str(member) in shown:
            continue
        stances: dict[str, set[str]] = {}
        for f in record.facts:
            if f.subject == member:
                for e in f.evidence:
                    stances.setdefault(e.block.split(":", 1)[0], set()).add(e.stance)
        entries.append(
            {
                "id": member,
                "sources": [
                    f"{doc} ({'copy' if 'copy' in st and 'supports' not in st else 'superseded' if st == {'superseded'} else 'contradicts' if st == {'contradicts'} else 'supports'})"
                    for doc, st in sorted(stances.items())
                ],
            }
        )
    return entries


def provenance_blocks(results: list[dict[str, Any]], record: Record, limit: int = 4) -> list[str]:
    """The source blocks of the copies, superseded and contradicting records that
    provenance_items asks the answer to explain: the writer is given what those documents say,
    so it explains the right document instead of another one with a similar role."""
    blocks: list[str] = []
    items = 0
    for r in results:
        for row in r["rows"]:
            listed = listed_entries(row, record)
            for entry in listed:
                docs = [
                    src.rpartition(" (")[0]
                    for src in entry.get("sources") or []
                    if isinstance(src, str)
                    and src.endswith(("(copy)", "(superseded)", "(contradicts)"))
                ]
                if not docs or items >= limit:
                    continue
                items += 1
                subject = str(entry.get("id") or "")
                for f in record.facts:
                    if f.subject == subject:
                        blocks += [
                            e.block
                            for e in f.evidence
                            if e.block.split(":", 1)[0] in docs and e.block not in blocks
                        ]
    return list(dict.fromkeys(blocks))[:12]


def provenance_items(results: list[dict[str, Any]], record: Record, limit: int = 4) -> list[str]:
    """Checklist items added by code: a returned item whose sources include a copy, a superseded
    record or a contradicting record must be explained, because duplicates and corrections change
    what is counted. Worded with document titles, not internal names."""
    titles = {d["key"]: (d.get("title") or d["key"].replace("_", " ")) for d in record.documents}
    items: list[str] = []
    seen: set[str] = set()
    for r in results:
        for row in r["rows"]:
            listed = listed_entries(row, record)
            for entry in listed:
                roles = []
                for src in entry.get("sources") or []:
                    if not isinstance(src, str) or not src.endswith(
                        ("(copy)", "(superseded)", "(contradicts)")
                    ):
                        continue
                    key, _, role = src.rpartition(" (")
                    roles.append(f"the {titles.get(key, key)} ({role.rstrip(')')})")
                item_id = str(entry.get("id") or "")
                if roles and item_id and item_id not in seen:
                    seen.add(item_id)
                    label = item_id[2:] if item_id.startswith("M:") else item_id
                    items.append(f"Explain how {', '.join(roles)} affects {label}")
    return items[:limit]


# --- one question ----------------------------------------------------------------------------


def _salvage(text: str) -> list[Any]:
    """A statement list the model serialized as text: parse it, or, when it is cut off, keep
    every complete statement object in it (never read it character by character)."""
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        pass
    decoder = json.JSONDecoder()
    found: list[Any] = []
    pos = text.find("{")
    while pos != -1:
        try:
            item, end = decoder.raw_decode(text, pos)
        except json.JSONDecodeError:
            pos = text.find("{", pos + 1)
            continue
        if isinstance(item, dict) and "text" in item:
            found.append(item)
        pos = text.find("{", end)
    return found or [text]


def normalize_answer(answer: Any) -> dict[str, Any]:
    """Coerce a malformed model answer into the expected shape; defects surface as check
    failures (for example a statement with no citations), never as crashes."""
    if not isinstance(answer, dict):
        answer = {"status": "partial", "statements": []}
    raw = answer.get("statements") or []
    if isinstance(raw, str):
        raw = _salvage(raw)
    elif (
        isinstance(raw, list)
        and len(raw) == 1
        and isinstance(raw[0], dict)
        and str(raw[0].get("text", "")).lstrip().startswith("[{")
    ):
        raw = _salvage(str(raw[0]["text"]))  # the whole list serialized into one statement
    statements = []
    for s in raw:
        if isinstance(s, str):
            s = {"text": s, "kind": "narrative", "cites": []}
        if not isinstance(s, dict) or not str(s.get("text", "")).strip():
            continue
        kind = (
            s.get("kind")
            if s.get("kind") in {"value", "conflict", "missing", "inference", "narrative"}
            else "narrative"
        )
        cites = [str(c) for c in (s.get("cites") or []) if isinstance(c, (str, int))]
        statements.append({"text": str(s["text"]), "kind": kind, "cites": cites})
    return {"status": answer.get("status", "answered"), "statements": statements}


def without_flagged(
    answer: dict[str, Any],
    issues: list[str],
    results: list[dict[str, Any]],
    record: Record,
    passages: dict[str, str],
    question: str,
    index: PassageIndex | None,
) -> tuple[dict[str, Any], list[str], list[str]]:
    """The answer without the statements that are still flagged (by code, or by the review as
    unsupported), re-checked by code. Only statements are removed, never rewritten; when a code
    finding is not tied to a statement, nothing is removed."""
    flagged = {
        int(m.group(1))
        for x in issues
        if (m := re.match(r"statement (\d+):", x.removeprefix(REVIEW)))
    }
    statements = answer.get("statements", [])
    if not flagged or any(
        not x.startswith("statement ") for x in issues if not x.startswith(REVIEW)
    ):
        return answer, issues, []
    kept = [st for n, st in enumerate(statements) if n not in flagged]
    if not kept:
        return answer, issues, []
    reduced = {**answer, "statements": kept}
    again, _ = code_check(
        json.loads(json.dumps(reduced)), results, record, passages, question, index
    )
    if again:
        return answer, issues, []
    removed = [statements[n]["text"][:120] for n in sorted(flagged) if n < len(statements)]
    return reduced, [], removed


def answer_question(
    qid: str, question: str, record: Record, policy: Policy, index: PassageIndex | None = None
) -> dict[str, Any]:
    started = time.monotonic()
    with llm.scope() as usage:
        try:
            answer = _answer_question(qid, question, record, policy, index)
        except Exception as error:  # one failing question is withheld, visibly; the run goes on
            answer = {
                "id": qid,
                "question": question,
                "status": "withheld",
                "reasons": [f"pipeline error: {type(error).__name__}: {error}"[:400]],
                "results": [],
                "plan": {},
            }
    seconds = round(time.monotonic() - started, 1)
    answer["usage"] = {
        **usage.as_dict(),
        "seconds": seconds,  # this run (cached calls are near instant)
        "cold_seconds": round(seconds + usage.cached_seconds, 1),  # as if nothing were cached
    }
    return answer


ABSENT = re.compile(
    r"\b(?:not (?:documented|recorded|stated|specified|given|named)|does not (?:document|record|"
    r"state|specify|name|give|include)|do not (?:document|record|state)|no (?:documented|recorded)|"
    r"(?:is|are|was|were) absent from the record|nowhere (?:documented|recorded|stated)|"
    r"no (?:\w+ ){1,3}(?:is|was|are|were) (?:documented|recorded|stated|given))\b|\(no \w+\)",
    re.I,
)
LOOKUP_KINDS = {"encounter", "measurement", "medication", "charge"}
# a dash, semicolon or colon between clauses
CLAUSE_BREAK = re.compile(r"\s+[—–]\s+|;\s+|:\s+")


def _event_day(facts: dict[str, Any]) -> str | None:
    for name in ("date", "completed_on"):
        f = facts.get(name)
        if f and f.value:
            return str(f.value)[:10]
    return next((str(f.valid_time)[:10] for f in facts.values() if f.valid_time), None)


def absence_in_facts(sentence: str, record: Record, policy: Policy) -> list[Any]:
    """Facts that document what a "not documented" sentence says is missing.

    The sentence's wording maps to fields (policy [absence]); the events are the ones it names by
    ID, or else by date, narrowed by the service, instrument or item it mentions. Only the clauses
    that make the claim are read: in "the record does not document whether the improvement is
    sustained — the January 16 score rests on one source", the January 16 score is context, not
    what is missing. A relative claim ("before January 5", "any other score") is not settled here;
    a claim left unsettled goes to the passage check."""
    claim = [c for c in CLAUSE_BREAK.split(sentence) if ABSENT.search(c)]
    sentence = " ".join(claim) or sentence
    low = sentence.lower()
    fields: set[str] = set()
    for word, names in policy.absence.items():
        if re.search(rf"\b{re.escape(word.lower())}\w*", low):
            fields |= set(names)
    identity = {"patient_mrn", "patient_dob", "patient_name"}
    # "no other / second MRN" is a claim about additional identifiers, not about the patient's own
    about_another = re.search(
        r"\b(?:other|another|second|different|additional|separate|new|alternate)\s+(?:\w+\s+){0,2}"
        r"(?:mrn|record number|identifier|date of birth|dob)",
        low,
    )
    if fields & identity and not about_another:
        # the patient's identity is one record-wide subject, stated in document headers
        patient = record.facts_of("patient")
        hits = [
            f
            for name in sorted(fields & identity)
            if (f := patient.get(name)) and f.value not in (None, "", [])
        ]
        if hits:
            return hits
    if any(re.search(rf"\b{re.escape(q)}\b", low) for q in policy.relative):
        return []
    if not fields:
        return []
    events = [e for e in record.events if e.kind in LOOKUP_KINDS]
    named = [e for e in events if re.search(rf"\b{re.escape(e.id.lower())}\b", low)]
    facts_of = {e.id: record.facts_of(e.id) for e in events}
    if not named:
        days = [str(f.value)[:10] for f in record.facts if f.field == "date" and f.value]
        if not days:
            return []
        first, last = date.fromisoformat(min(days)), date.fromisoformat(max(days))
        said = {d.isoformat() for d in find_dates(sentence, first, last, expand=False)}
        if not said:
            return []
        on_day = [e for e in events if _event_day(facts_of[e.id]) in said]
        words = policy.categories(sentence) if policy.service(sentence) else set()
        item = re.search(r"\bitem\s*(\d+)", low)

        def fits(e: Any) -> bool:
            f = facts_of[e.id]
            if e.kind == "measurement":
                instrument = str(f["instrument"].value).lower() if f.get("instrument") else ""
                if instrument and instrument not in low:
                    return False
                has_item = f.get("item") and f["item"].value not in (None, "")
                if item:
                    return bool(has_item and str(f["item"].value).strip() == item.group(1))
                return not has_item
            if e.kind == "encounter":
                service = str(f["service"].value) if f.get("service") else ""
                return not words or service in words
            return e.kind in low or (e.kind == "medication" and "medication" in low)

        named = [e for e in on_day if fits(e)]
        if len(named) > 1 and not words and not item:
            return []  # the sentence does not say which of several events it means
    hits = []
    for e in named:
        for name in sorted(fields):
            f = facts_of[e.id].get(name)
            if f and f.status != "not_documented" and f.value not in (None, "", []):
                hits.append(f)
    return hits


def _states_value(text: str, fact: Any) -> bool:
    numbers = stated(text, [])[0]
    for v in fact.values():
        try:
            if round(float(v), 2) in numbers:
                return True
        except (TypeError, ValueError):
            if str(v).lower() in text.lower():
                return True
    return False


def absence_sentences(text: str) -> list[str]:
    """Sentences of a statement that claim the record lacks something."""
    return [x.strip() for x in re.split(r"(?<=[.;])\s+", text) if ABSENT.search(x)]


STRAY_DATE = re.compile(r"^statement (\d+): date ([0-9, -]+) is not a date of its cited evidence")


def repair_dates(
    answer: dict[str, Any], issues: list[str], passages: dict[str, str], index: PassageIndex | None
) -> list[str]:
    """Fix date-binding failures without a model. For each stray date, the passage that names
    that date and best matches the sentence is cited; if no passage does, the sentence carrying
    the date is dropped and the rest of the statement kept. Returns what was done."""
    done: list[str] = []
    statements = answer.get("statements", [])
    for issue in issues:
        m = STRAY_DATE.match(issue)
        if not m or int(m.group(1)) >= len(statements):
            continue
        s = statements[int(m.group(1))]
        for day in [d.strip() for d in m.group(2).split(",") if d.strip()]:
            target = date.fromisoformat(day)
            sentences = re.split(r"(?<=[.;])\s+", s["text"])
            carrying = [x for x in sentences if target in find_dates(x, target, target)]
            query = " ".join(carrying) or s["text"]
            hit = None
            if index is not None:
                for p in index.search(query, k=12):
                    if target in find_dates(index.text(p["id"]) or "", target, target):
                        hit = p
                        break
            if hit:
                if hit["id"] not in s["cites"]:
                    s["cites"].append(hit["id"])
                    s.setdefault("added_cites", []).append(hit["id"])
                passages[hit["id"]] = index.text(hit["id"]) or "" if index else ""
                done.append(f"statement {m.group(1)}: cited {hit['id']} for {day}")
            elif carrying and len(carrying) < len(sentences):
                s["text"] = " ".join(x for x in sentences if x not in carrying)
                s.setdefault("dropped", []).extend(carrying)
                done.append(f"statement {m.group(1)}: dropped the clause dated {day}")
    return done


QUANTITY = re.compile(
    r"\b(?:percent(?:age)?|change|difference|increase|decrease|reduction|drop|total|sum|"
    r"average|mean|count|number of|how many)\b",
    re.I,
)
GAP_ISSUE = "an answer called this missing, but the record may hold it; add a query that "


def computable_gaps(answer: dict[str, Any], record: Record) -> list[str]:
    """ "Missing" statements that name a quantity of something the record holds (a measure it
    has scores for, or encounter minutes, days or sessions): the query language can usually
    compute those (change(), percent_change(), sum(), count()), so the question is re-planned
    once with the gap before the claim is accepted."""
    instruments = {
        str(f.value).lower() for f in record.facts if f.field == "instrument" and f.value
    }
    held = re.compile(
        r"\b(?:minutes?|days?|sessions?|visits?|encounters?|scores?)\b"
        + "".join(f"|{re.escape(i)}" for i in sorted(instruments)),
        re.I,
    )
    return [
        GAP_ISSUE + f'computes it: "{st["text"][:200]}"'
        for st in answer.get("statements", [])
        if st["kind"] == "missing" and QUANTITY.search(st["text"]) and held.search(st["text"])
    ]


UNBOUND = re.compile(r"^statement (\d+): ([\d., ]+) is in no cited result")


def uncomputed_figures(answer: dict[str, Any], issues: list[str]) -> list[str]:
    """A change, percentage or total the writer had to work out itself because no query computed
    it: the planner is asked once for a query that computes it (the writer never may)."""
    statements = answer.get("statements", [])
    out = []
    for issue in issues:
        m = UNBOUND.match(issue)
        if not m or int(m.group(1)) >= len(statements):
            continue
        text = statements[int(m.group(1))]["text"]
        if QUANTITY.search(text):
            out.append(
                f"the answer needed {m.group(2).strip()} but no query computes it; add a query "
                f"that does (for example change()/percent_change() over exactly the dates named, "
                f'or sum()/count()): "{text[:200]}"'
            )
    return out


def _population_warnings(model_issues: list[str]) -> list[str]:
    """A population finding re-plans the question once; it never withholds an answer (the
    reviewer can mistake a context query for the counted one), so afterwards it is a warning."""
    return [m for m in model_issues if m.startswith(POPULATION_ISSUE)]


def _code_only(issues: list[str], model_issues: list[str]) -> bool:
    """Every remaining failure is a code finding that names its fix."""
    return bool(issues) and not model_issues


def final_status(
    issues: list[str], model_issues: list[str], writer_status: str, gaps_stated: bool = True
) -> str:
    """Code findings and model-judged errors withhold the answer. When all that is left after the
    repair is the reviewer's view that a part or checklist item is not covered, every statement
    has passed its checks, so the answer is published as partial with those gaps listed. An
    answer the writer calls partial is answered when the review finds every part covered and the
    answer states no gap ("not documented") that would make it partial."""
    if issues:
        return "withheld"
    if not model_issues:
        return "answered" if writer_status == "partial" and not gaps_stated else writer_status
    if all(m.startswith((PART_ISSUE, CHECKLIST_ISSUE, COVERAGE_ISSUE)) for m in model_issues):
        return "partial"
    return "withheld"


def _checks(
    question: str,
    plan: dict[str, Any],
    answer: dict[str, Any],
    results: list[dict[str, Any]],
    record: Record,
    passages: dict[str, str],
    index: PassageIndex | None,
    policy: Policy | None = None,
    review: tuple[list[str], dict[str, Any]] | None = None,
) -> tuple[list[str], list[str], dict[str, Any], list[dict[str, Any]]]:
    """Code checks, the small model's review, then absence verification of every "not
    documented" claim (first against the facts table by code, then against the source passages)
    and of every question part the review says is unanswered."""
    issues, attach = code_check(
        answer,
        results,
        record,
        passages,
        question,
        index,
        [t for t in plan.get("required_totals") or [] if isinstance(t, dict)],
    )
    # a code repair only adds citations or drops a clause, so the review of the rest stands
    model_issues, verdict = (
        (
            [m for m in review[0] if not m.startswith((COVERAGE_ISSUE, STYLE_ISSUE))],
            dict(review[1]),
        )
        if review is not None
        else model_check(question, plan, answer, results, record, passages, index)
    )
    model_issues += audit_coverage(answer, results) + jargon(answer, record)
    found: list[dict[str, Any]] = []
    if index is not None:
        statements = answer.get("statements", [])
        # every absence claim is verified, whatever kind of statement it sits in ("... 90 minutes.
        # The record does not document a duration for the collateral contact.")
        missing = [(n, st["text"]) for n, st in enumerate(statements) if st["kind"] == "missing"]
        missing += [
            (n, sentence)
            for n, st in enumerate(statements)
            if st["kind"] != "missing"
            for sentence in absence_sentences(st["text"])
        ]
        if policy is not None:
            # the facts table first: a reconciled value settles the claim without a model
            settled = set()
            for n, text in missing:
                sentences = absence_sentences(text)
                hits = [
                    f
                    for x in sentences
                    for f in absence_in_facts(x, record, policy)
                    if not _states_value(text, f)  # the statement already gives this value
                ]
                if hits:
                    settled.add((n, text))
                    shown = "; ".join(
                        f"{f.id}: {f.subject} {f.field} = "
                        + (
                            " or ".join(map(str, f.values()))
                            if f.status == "conflicting"
                            else str(f.value)
                        )
                        + (f" ({f.reason[:80]})" if f.reason else "")
                        for f in hits[:4]
                    )
                    issues.append(
                        f"statement {n}: says the record does not document this, but the record "
                        f"has {shown}; state it and cite the fact"
                    )
            missing = [m for m in missing if m not in settled]
        unaddressed = [m for m in model_issues if m.startswith((PART_ISSUE, CHECKLIST_ISSUE))]
        parts = [m.split(": ", 1)[1] for m in unaddressed]
        checks = verify_absence([t for _, t in missing] + parts, question, index)
        for (n, _text), result in zip(missing, checks[: len(missing)], strict=False):
            if result["documented"]:
                found.append(result)
                issues.append(
                    f"statement {n}: says the record does not document this, but passage "
                    f"{result['passage']} states: {result.get('quote') or ''}"[:400]
                )
        for complaint, result in zip(unaddressed, checks[len(missing) :], strict=False):
            if result["documented"]:
                found.append(result)
                continue
            # the source has nothing on it: saying it is not documented answers that part
            if missing:
                model_issues = [m for m in model_issues if m != complaint]
        if missing or parts:
            verdict = {**verdict, "absence_checks": checks}
    return issues, model_issues, verdict, found


# The time budget of one answer. The first plan, answer and check always run; each further model
# step (a re-plan, a repair) starts only when the time left covers it. When no step fits,
# statements still flagged are removed rather than repaired, so nothing unchecked is shown.
ANSWER_SECONDS = 90.0
REPLAN_SECONDS = 60.0  # time a second plan-and-answer pass needs
REPAIR_SECONDS = 40.0  # time a model repair, its re-check and framing need


def _answer_question(
    qid: str,
    question: str,
    record: Record,
    policy: Policy,
    index: PassageIndex | None = None,
    feedback: list[str] | None = None,
    deadline: float | None = None,
) -> dict[str, Any]:
    deadline = deadline or time.monotonic() + ANSWER_SECONDS
    plan, results, query_errors = plan_and_execute(question, record, policy, feedback)
    if query_errors and not results:
        return {
            "id": qid,
            "question": question,
            "status": "withheld",
            "reasons": ["queries failed: " + "; ".join(query_errors)],
            "plan": plan,
            "results": [],
        }
    if (
        plan.get("explain_counts") is True
        and EXPLAIN_COUNTS.search(question)
        and (audit := count_audit(results, record))
    ):
        results = results + [audit]
    facts, open_items = record_context(results, record, question)
    plan["checklist"] = list(plan.get("checklist", [])) + provenance_items(results, record)
    found_passages = index.search(question, k=8) if index else []
    if index is not None:
        # the documents code asks the answer to explain come with their own text: the blocks
        # behind the facts, then the rest of each such document (a copy usually says what it is)
        known = {p["id"] for p in found_passages}
        behind = provenance_blocks(results, record)
        documents = list(dict.fromkeys(b.split(":", 1)[0] for b in behind))
        whole = [
            bid
            for doc in documents
            for bid, _name, _text in index.blocks
            if bid.startswith(f"{doc}:")
        ][: 8 * len(documents)]
        found_passages += [
            {"id": b, "file": index.by_id[b][0], "text": (index.text(b) or "")[:700]}
            for b in dict.fromkeys(behind + whole)
            if b not in known and index.text(b)
        ]
    passages = {p["id"]: p["text"] for p in found_passages}
    base = {
        "question": question,
        "checklist": plan.get("checklist", []),
        "results": compact_results(results),
        "facts": facts,
        "open_items": open_items,
        "passages": found_passages,
    }
    answer = normalize_answer(
        llm.call("answer", ANSWER, json.dumps(base, default=str), ANSWER_SCHEMA, llm.WRITER, 6000)
    )
    issues, model_issues, verdict, found = _checks(
        question, plan, answer, results, record, passages, index, policy
    )
    mismatch = [m for m in model_issues if m.startswith(POPULATION_ISSUE)]
    gaps = computable_gaps(answer, record) + uncomputed_figures(answer, issues)
    if (mismatch or gaps) and not feedback and deadline - time.monotonic() > REPLAN_SECONDS:
        # the queries counted the wrong set, or the answer calls a quantity missing that the
        # query language can compute from the record: re-plan once with that, then answer anew
        again = _answer_question(qid, question, record, policy, index, mismatch + gaps, deadline)
        again["replanned"] = mismatch + gaps
        return again
    warnings = _population_warnings(model_issues)
    model_issues = [m for m in model_issues if m not in warnings]
    history = [{"answer": answer, "code_issues": issues, "model_issues": model_issues}]
    repairs = 0
    while issues or model_issues:
        fixed = repair_dates(answer, issues, passages, index)
        if fixed:
            # code repaired what it could prove; re-check before asking the model
            base["passages"] = base["passages"] + [
                {"id": c, "text": passages[c][:700]}
                for c in {x.split(" cited ")[1].split(" for ")[0] for x in fixed if " cited " in x}
                if c in passages and c not in {p["id"] for p in base["passages"]}
            ]
            issues, model_issues, verdict, found = _checks(
                question,
                plan,
                answer,
                results,
                record,
                passages,
                index,
                policy,
                review=(model_issues, verdict),
            )
            history.append(
                {"code_repair": fixed, "code_issues": issues, "model_issues": model_issues}
            )
            if not (issues or model_issues):
                break
        # one model repair; a second only when every remaining failure is a code finding with a
        # specific hint
        if repairs == 1 and not _code_only(issues, model_issues):
            break
        if repairs == 2 or deadline - time.monotonic() < REPAIR_SECONDS:
            break
        repairs += 1
        # passages that document what the answer called missing join the evidence
        for f in found:
            if f["passage"] and f["passage"] not in passages and index:
                text = index.text(f["passage"]) or ""
                passages[f["passage"]] = text
                base["passages"] = base["passages"] + [{"id": f["passage"], "text": text[:700]}]
        repair = {
            **base,
            "previous_answer": answer,
            "issues": issues + model_issues,
            "instruction": "Fix exactly these issues and return the complete answer. Cite the "
            "result or fact that states each flagged number, or remove the number; when a passage "
            "or fact documents something you called missing, answer from it and cite it; delete "
            "a flagged statement the question does not need rather than keeping an unsupported claim.",
        }
        answer = normalize_answer(
            llm.call(
                "repair", ANSWER, json.dumps(repair, default=str), ANSWER_SCHEMA, llm.WRITER, 6000
            )
        )
        issues, model_issues, verdict, found = _checks(
            question, plan, answer, results, record, passages, index, policy
        )
        warnings += _population_warnings(model_issues)
        model_issues = [m for m in model_issues if not m.startswith(POPULATION_ISSUE)]
        history.append({"answer": answer, "code_issues": issues, "model_issues": model_issues})
    unsupported = [f"{REVIEW}{m}" for m in model_issues if m.startswith("statement ")]
    if (issues or unsupported) and len(answer.get("statements", [])) > 1:
        # out of repairs or time: remove the statements still flagged (by code, or by the review
        # as unsupported); the rest are re-checked by code
        answer, left, removed = without_flagged(
            answer, issues + unsupported, results, record, passages, question, index
        )
        if removed:
            issues = [x for x in left if not x.startswith(REVIEW)]
            warnings += removed
            model_issues = [m for m in model_issues if not m.startswith("statement ")]
            model_issues += [f"{CHECKLIST_ISSUE}removed as unverified: {r}" for r in removed]
    # a style finding left after the repair is reported, never withheld
    warnings += [m for m in model_issues if m.startswith(STYLE_ISSUE)]
    model_issues = [m for m in model_issues if not m.startswith(STYLE_ISSUE)]
    _, attach = code_check(
        json.loads(json.dumps(answer)), results, record, passages, question, index
    )
    status = final_status(
        issues,
        model_issues,
        answer.get("status", "answered"),
        any(st.get("kind") == "missing" for st in answer.get("statements", [])),
    )
    if status != "withheld":
        answer = framed(question, answer)
    return {
        "id": qid,
        "question": question,
        "status": status,
        "reasons": issues + model_issues,
        "answer": answer,
        "attached_results": attach,
        "plan": plan,
        "query_errors": query_errors,
        "warnings": sorted(set(warnings)),
        "results": results,
        "passages": base["passages"],
        "history": history,
        "check": verdict,
    }


# --- framing: what goes out -------------------------------------------------------------------

FRAME = """You decide which statements of a checked answer go out as the answer to the question.
The statements are already verified; you only select and order them, never rewrite them.
Split the question into the separate things it asks (the same parts a reader would tick off).
For each part, list the statements that answer it. Then choose:
- lead: the statements that directly answer the question, most direct first;
- context: statements a reader needs to read the lead correctly and only those: a conflict or
  gap about a figure the lead states, a partial week, a count's scope when the question names it.
Leave out everything the question did not ask about (background, treatment, goals, outcomes,
course of care, other weeks or services), however true. A question that asks one thing usually
needs one to three statements."""

FRAME_SCHEMA = {
    "type": "object",
    "properties": {
        "parts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "part": {"type": "string"},
                    "statements": {"type": "array", "items": {"type": "integer"}},
                },
                "required": ["part", "statements"],
            },
        },
        "lead": {"type": "array", "items": {"type": "integer"}},
        "context": {"type": "array", "items": {"type": "integer"}},
    },
    "required": ["parts", "lead", "context"],
}


def frame(question: str, answer: dict[str, Any]) -> dict[str, Any]:
    """Select and order the checked statements that answer the question. Code keeps every
    question part answered and never drops a conflict or gap about what the lead states; the
    rest is held back (kept for audit, not shown). On any failure every statement is kept."""
    statements = answer.get("statements", [])
    if len(statements) <= 1:
        return {"lead": list(range(len(statements))), "context": [], "omitted": [], "parts": []}
    listing = [{"index": i, "kind": s["kind"], "text": s["text"]} for i, s in enumerate(statements)]
    try:
        out = llm.call(
            "frame",
            FRAME,
            json.dumps({"question": question, "statements": listing}),
            FRAME_SCHEMA,
            llm.SMALL,
            2000,
        )
    except llm.ModelError:
        out = {}
    valid = range(len(statements))
    lead = [i for i in dict.fromkeys(out.get("lead") or []) if i in valid]
    if not lead:
        return {"lead": list(valid), "context": [], "omitted": [], "parts": []}
    context = [i for i in dict.fromkeys(out.get("context") or []) if i in valid and i not in lead]
    kept = set(lead) | set(context)
    parts = [
        {
            "part": str(p.get("part", "")),
            "statements": [i for i in p.get("statements") or [] if i in valid],
        }
        for p in llm.as_list(out.get("parts"), ("part",))
    ]
    # every part the question asks keeps an answer
    for p in parts:
        if p["statements"] and not kept & set(p["statements"]):
            context.append(p["statements"][0])
            kept.add(p["statements"][0])
    # a conflict or gap about something a kept statement cites stays with it
    cited = {c for i in kept for c in statements[i].get("cites", [])}
    for i, s in enumerate(statements):
        if (
            i not in kept
            and s["kind"] in {"conflict", "missing"}
            and cited & set(s.get("cites", []))
        ):
            context.append(i)
            kept.add(i)
    omitted = [i for i in valid if i not in kept]
    return {"lead": lead, "context": sorted(context), "omitted": omitted, "parts": parts}


def framed(question: str, answer: dict[str, Any]) -> dict[str, Any]:
    """The answer as published: lead then context; held-back statements under `omitted`."""
    selection = frame(question, answer)
    statements = answer.get("statements", [])
    order = selection["lead"] + selection["context"]
    return {
        **answer,
        "statements": [statements[i] for i in order],
        "omitted": [statements[i] for i in selection["omitted"]],
        "framing": selection,
    }


def run_stats(answers: list[dict[str, Any]]) -> dict[str, Any]:
    """Cost and time per question and in total, labelled two ways. this_run: what this run paid
    and how long it took (cached calls are free and near instant). cold: what the answers cost
    and took to produce from nothing (cached calls counted at their original cost and model time;
    exact for calls cached with their usage and timing)."""

    def usage(a: dict[str, Any], key: str, default: float = 0.0) -> float:
        return float(a.get("usage", {}).get(key) or default)

    per = [
        {
            "id": a["id"],
            "status": a["status"],
            "calls": int(usage(a, "calls") + usage(a, "cached")),
            "this_run": {"cost_usd": usage(a, "cost_usd"), "seconds": usage(a, "seconds")},
            "cold": {
                "cost_usd": usage(a, "full_cost_usd"),
                "seconds": usage(a, "cold_seconds", usage(a, "seconds")),
            },
        }
        for a in answers
    ]

    def summary(kind: str) -> dict[str, Any]:
        seconds = sorted(p[kind]["seconds"] for p in per)
        return {
            "cost_usd": round(sum(p[kind]["cost_usd"] for p in per), 4),
            "median_seconds": seconds[len(seconds) // 2] if seconds else None,
            "max_seconds": seconds[-1] if seconds else None,
        }

    cached = sum(int(usage(a, "cached")) for a in answers)
    calls = sum(int(usage(a, "calls")) for a in answers)
    return {
        "questions": len(per),
        # how this run's own timing was made: cold (no cached calls), cached or partly cached
        "timing": "cold" if cached == 0 else "cached" if calls == 0 else "partly cached",
        "model_calls": calls,
        "cached_calls": cached,
        "this_run": summary("this_run"),
        "cold": summary("cold"),
        "per_question": per,
    }


def ask_all(
    documents: list[Document],
    policy: Policy,
    out: Path,
    questions_path: Path,
    ids: list[str] | None,
    workers: int,
) -> None:
    from record_engine.render import answers_markdown

    record = Record.model_validate_json((out / "abstraction.json").read_text())
    questions = json.loads(questions_path.read_text())
    if ids:
        questions = [q for q in questions if q["id"] in ids]
    index = PassageIndex(documents)
    with ThreadPoolExecutor(min(workers, 4)) as pool:
        answers = list(
            pool.map(
                llm.carry(lambda q: answer_question(q["id"], q["question"], record, policy, index)),
                questions,
            )
        )
    (out / "answers.json").write_text(json.dumps(answers, indent=1, default=str))
    (out / "run_stats.json").write_text(json.dumps(run_stats(answers), indent=1))
    (out / "answers.md").write_text(answers_markdown(answers, record, documents))


def _result_rows(results: list[dict[str, Any]], result_id: str) -> list[dict[str, Any]]:
    return [row for r in results if r["id"] == result_id for row in r["rows"]]
