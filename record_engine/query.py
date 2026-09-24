"""⑦ A small query language over the record, executed by code with scenario arithmetic.

    from encounters
    where date >= 2026-03-02 and date <= 2026-03-27 and disposition = included
    group_by week
    select count(), count_distinct(date), sum(minutes), goal_met()

Sources: encounters, references (entries that document no visit), charges, measurements,
medications, findings, goals, facts, open_items.
Conditions: field (= != > >= < <= contains) value, field in (a, b), field in goal.services;
field = none / field != none test for an empty field; combine with and, or, parentheses.
group_by: week | week(tuesday) | service | date | month | instrument | subject | type | reporter.
select: field (its values) count() count_distinct(f) sum(f) min(f) max(f) first(f) last(f) list(f, ...)
        change(f) percent_change(f) days_between() goal_met() rows()
days_between() is the days from the group's first dated row to its last.

Values are sets of scenarios: sum({40, 50}, 300) = {340, 350}. Independent conflicts combine as a
Cartesian product and collapse to the two endpoints above the policy limit (flagged); goal_met()
keeps every scenario. Every result
row carries the fact IDs it used; rows the window admitted but a condition excluded are listed
with the failing condition, so inclusions and exclusions are visible.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

from record_engine.model import Record
from record_engine.policy import Policy

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
SOURCES = {
    "encounters",
    "charges",
    "references",
    "measurements",
    "medications",
    "findings",
    "goals",
    "facts",
    "open_items",
}
# Encounter-like entries that document no visit: a booking, template, charge or reference to a
# visit recorded elsewhere, or chart handling. They are listed under "references", not encounters.
REFERENCE_DISPOSITIONS = {"no_actual_record", "not_care"}
AGGREGATES = {
    "count",
    "count_distinct",
    "sum",
    "min",
    "max",
    "first",
    "last",
    "list",
    "change",
    "percent_change",
    "days_between",
    "goal_met",
    "rows",
}
TOKEN = re.compile(
    r"\s*(?:(?P<str>'[^']*'|\"[^\"]*\")|(?P<op>>=|<=|!=|=|>|<)|(?P<punct>[(),])|(?P<word>[^\s(),=<>!]+))"
)


class QueryError(ValueError):
    pass


@dataclass
class Condition:
    field: str
    op: str
    value: Any


@dataclass
class AnyOf:
    """A disjunction of conjunctions: (a and b) or c."""

    options: list[list[Any]]
    field: str = "(or)"
    op: str = "or"
    value: Any = None

    def __str__(self) -> str:
        return " or ".join(
            "(" + " and ".join(str(getattr(c, "field", c)) for c in conj) + ")"
            for conj in self.options
        )


@dataclass
class Aggregate:
    name: str
    args: list[str]

    def label(self) -> str:
        if self.name == "values":
            reserved = {"id", "group", "groups", "members", "facts", "partial_week", "covered"}
            return f"{self.args[0]}_values" if self.args[0] in reserved else self.args[0]
        return f"{self.name}({', '.join(self.args)})"


@dataclass
class Query:
    source: str
    where: list[Condition] = field(default_factory=list)
    group_by: str | None = None
    select: list[Aggregate] = field(default_factory=list)
    text: str = ""


# --- parsing ---------------------------------------------------------------------------------


def tokenize(text: str) -> list[str]:
    tokens, pos = [], 0
    text = text.strip()
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m or m.end() == pos:
            raise QueryError(f"cannot read query near {text[pos : pos + 20]!r}")
        pos = m.end()
        tokens.append(m.group(0).strip())
    return [t for t in tokens if t]


def literal(token: str) -> Any:
    if token[:1] in {"'", '"'}:
        return token[1:-1]
    try:
        return date.fromisoformat(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        return token


def _parse_condition(tokens: list[str], i: int) -> tuple[Condition, int]:
    if i + 2 > len(tokens):
        raise QueryError("incomplete condition")
    name, op = tokens[i], tokens[i + 1].lower()
    if op == "in":
        if i + 2 < len(tokens) and tokens[i + 2] == "(":
            j = i + 3
            values = []
            while j < len(tokens) and tokens[j] != ")":
                if tokens[j] != ",":
                    values.append(literal(tokens[j]))
                j += 1
            if j >= len(tokens):
                raise QueryError("missing ) in 'in' list")
            return Condition(name, "in", values), j + 1
        if i + 2 >= len(tokens):
            raise QueryError(f"missing set after {name} in")
        return Condition(name, "in", tokens[i + 2]), i + 3
    if op in {"=", "!=", ">", ">=", "<", "<=", "contains"}:
        if i + 2 >= len(tokens):
            raise QueryError(f"missing value after {name} {op}")
        return Condition(name, op, literal(tokens[i + 2])), i + 3
    raise QueryError(f"unknown operator {op!r}")


def _parse_or(tokens: list[str], i: int) -> tuple[list[list[Any]], int]:
    """expr := conj ('or' conj)* ; conj := factor ('and' factor)* ; factor := '(' expr ')' | cond"""
    options: list[list[Any]] = []
    while True:
        conj: list[Any] = []
        while True:
            if i < len(tokens) and tokens[i] == "(":
                inner, i = _parse_or(tokens, i + 1)
                if i >= len(tokens) or tokens[i] != ")":
                    raise QueryError("missing ) in where clause")
                i += 1
                conj.append(inner[0][0] if len(inner) == 1 and len(inner[0]) == 1 else AnyOf(inner))
            else:
                cond, i = _parse_condition(tokens, i)
                conj.append(cond)
            if i < len(tokens) and tokens[i].lower() == "and":
                i += 1
                continue
            break
        options.append(conj)
        if i < len(tokens) and tokens[i].lower() == "or":
            i += 1
            continue
        return options, i


def _parse_where(tokens: list[str], i: int) -> tuple[list[Any], int]:
    options, i = _parse_or(tokens, i)
    if len(options) == 1:
        flat: list[Any] = []
        for item in options[0]:
            flat.append(item)
        return flat, i
    return [AnyOf(options)], i


def parse(text: str) -> Query:
    tokens = tokenize(text)
    if len(tokens) < 2 or tokens[0].lower() != "from":
        raise QueryError("a query starts with: from <source>")
    source = tokens[1].lower()
    if source not in SOURCES:
        raise QueryError(f"unknown source {source!r}; use one of {sorted(SOURCES)}")
    q = Query(source=source, text=text)
    i = 2

    def peek() -> str | None:
        return tokens[i].lower() if i < len(tokens) else None

    while i < len(tokens):
        word = tokens[i].lower()
        if word == "where":
            items, i = _parse_where(tokens, i + 1)
            q.where.extend(items)
        elif word == "group_by":
            if i + 1 >= len(tokens):
                raise QueryError("group_by needs a key")
            key = tokens[i + 1].lower()
            i += 2
            if key == "week" and peek() == "(":
                key = f"week({tokens[i + 1].lower()})"
                i += 3
            q.group_by = key
        elif word == "select":
            i += 1
            while i < len(tokens):
                name = tokens[i].lower()
                if name not in AGGREGATES and (i + 1 >= len(tokens) or tokens[i + 1] != "("):
                    # a bare field name: the distinct values of that field in the group
                    q.select.append(Aggregate("values", [tokens[i]]))
                    i += 1
                    if peek() == ",":
                        i += 1
                        continue
                    break
                if name not in AGGREGATES:
                    raise QueryError(f"unknown function {name!r}; use one of {sorted(AGGREGATES)}")
                if i + 1 >= len(tokens) or tokens[i + 1] != "(":
                    raise QueryError(f"{name} needs parentheses")
                j = i + 2
                args = []
                while j < len(tokens) and tokens[j] != ")":
                    if tokens[j] != ",":
                        args.append(tokens[j])
                    j += 1
                if j >= len(tokens):
                    raise QueryError(f"missing ) after {name}")
                q.select.append(Aggregate(name, args))
                i = j + 1
                if peek() == ",":
                    i += 1
                    continue
                # a missing comma before another function call is unambiguous: read on
                if peek() in AGGREGATES and i + 1 < len(tokens) and tokens[i + 1] == "(":
                    continue
                break
        else:
            raise QueryError(f"unexpected {tokens[i]!r}; expected where, group_by or select")
    if not q.select:
        q.select = [Aggregate("rows", [])]
    return q


# --- scenario values -------------------------------------------------------------------------


@dataclass
class Scenarios:
    values: list[float]
    collapsed: bool = False

    def __post_init__(self) -> None:
        self.values = sorted(set(self.values))


def combine(a: Scenarios, b: Scenarios, limit: int) -> Scenarios:
    values = {x + y for x in a.values for y in b.values}
    if len(values) > limit:
        return Scenarios([min(values), max(values)], True)
    return Scenarios(list(values), a.collapsed or b.collapsed)


# --- rows ------------------------------------------------------------------------------------


def rows_for(source: str, record: Record) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for event in record.events:
        facts = record.facts_of(event.id)

        def val(name: str, facts: dict[str, Any] = facts) -> Any:
            f = facts.get(name)
            if f is None:
                return None
            if f.status == "conflicting" and f.scenarios:
                return (
                    Scenarios([float(v) for v in f.scenarios])
                    if all(isinstance(v, (int, float)) for v in f.scenarios)
                    else list(f.scenarios)
                )
            return f.value

        ids = [f.id for f in facts.values()]
        # which documents support this item, and in what role (copies and reports are marked)
        roles: dict[str, set[str]] = {}
        for f in facts.values():
            for e in f.evidence:
                roles.setdefault(e.block.split(":", 1)[0], set()).add(e.stance)
        sources = sorted(
            f"{doc} ({'copy' if 'copy' in st and 'supports' not in st else 'superseded' if st == {'superseded'} else 'contradicts' if st == {'contradicts'} else 'supports'})"
            for doc, st in roles.items()
        )
        if (
            source == "references"
            and event.kind == "encounter"
            and val("disposition") in REFERENCE_DISPOSITIONS
        ):
            disposition = facts.get("disposition")
            rows.append(
                {
                    "id": event.id,
                    "date": _date(val("date")),
                    "service": val("service"),
                    "kind": val("disposition"),
                    "why": disposition.reason if disposition else "",
                    "sources": sources,
                    "_facts": ids,
                }
            )
        if (
            source == "encounters"
            and event.kind == "encounter"
            and val("disposition") not in REFERENCE_DISPOSITIONS
        ):
            day = val("date")
            minutes = facts.get("minutes")
            rows.append(
                {
                    "id": event.id,
                    "date": _date(day),
                    "service": val("service"),
                    "attendance": val("attendance"),
                    "appointment_status": val("status"),
                    # did the patient receive the service at all (partial attendance counts)
                    "delivered": "uncertain"
                    if isinstance(val("attendance"), list)
                    else "yes"
                    if val("attendance") == "attended"
                    else "no"
                    if val("attendance") == "not_attended"
                    else None,
                    "disposition": val("disposition"),
                    "minutes": Scenarios([float(v) for v in minutes.values()])
                    if minutes and minutes.status != "not_documented"
                    else None,
                    "session_minutes": Scenarios(
                        [float(v) for v in facts["session_minutes"].values()]
                    )
                    if facts.get("session_minutes")
                    else None,
                    "scheduled": val("scheduled"),
                    "participants": val("participants"),
                    "mode": val("mode"),
                    "status_reason": val("status_reason"),
                    "status": "conflicting"
                    if any(f.status == "conflicting" for f in facts.values())
                    else (minutes.status if minutes else "documented"),
                    "records": val("records"),
                    "sources": sources,
                    "_facts": ids,
                }
            )
        elif source == "charges" and event.kind == "charge":
            rows.append(
                {
                    "id": event.id,
                    **{
                        k: val(k)
                        for k in (
                            "charge_id",
                            "encounter_id",
                            "service",
                            "code",
                            "quantity",
                            "status",
                            "amount",
                        )
                    },
                    "date": _date(val("date")),
                    "sources": sources,
                    "_facts": ids,
                }
            )
        elif source == "measurements" and event.kind == "measurement":
            score = facts.get("score")
            rows.append(
                {
                    "id": event.id,
                    "instrument": val("instrument"),
                    "item": val("item"),
                    "score": Scenarios([float(v) for v in score.values()]) if score else None,
                    "date": _date(val("completed_on")),
                    "status": score.status if score else "not_documented",
                    "sources": sources,
                    "_facts": ids,
                }
            )
        elif source == "medications" and event.kind == "medication":
            rows.append(
                {
                    "id": event.id,
                    **{k: val(k) for k in ("name", "dose", "schedule", "change")},
                    "date": _date(val("date")),
                    "_facts": ids,
                }
            )
        elif source == "findings" and event.kind == "finding":
            rows.append(
                {
                    "id": event.id,
                    **{k: val(k) for k in ("text", "type", "reporter", "encounter_id")},
                    "date": _date(val("date")),
                    "_facts": ids,
                }
            )
        elif source == "goals" and event.kind == "goal":
            rows.append(
                {
                    "id": event.id,
                    **{
                        k: val(k)
                        for k in (
                            "basis",
                            "target",
                            "threshold",
                            "comparator",
                            "unit",
                            "period",
                            "week_start",
                            "eligible_services",
                            "excluded_services",
                            "effective_start",
                            "effective_end",
                        )
                    },
                    "sources": sources,
                    "_facts": ids,
                }
            )
    if source == "facts":
        rows = [
            {
                "id": f.id,
                "subject": f.subject,
                "field": f.field,
                "value": f.value if f.status != "conflicting" else list(f.scenarios),
                "status": f.status,
                "rule": f.rule,
                "date": _date(f.valid_time),
                "_facts": [f.id],
            }
            for f in record.facts
        ]
    if source == "open_items":
        # patient-record items only; extraction-quality items (rejected values, uncaptured
        # mentions) are reported in the abstraction, not answered from
        rows = [
            {
                "id": f"OI-{n}",
                "kind": o.kind,
                "subject": o.subject,
                "text": o.text,
                "_facts": o.facts,
            }
            for n, o in enumerate(record.open_items)
            if o.kind in {"conflict", "missing", "candidate_link"}
        ]
    # computed by code, so no one works a weekday out by hand
    for row in rows:
        if isinstance(row.get("date"), date):
            row["weekday"] = row["date"].strftime("%A")
    if source in {"encounters", "references", "measurements", "charges"}:
        # the documents that record each item (linked-document groups), by their own IDs
        doc_ids = {
            f.subject[2:]: str(f.value)
            for f in record.facts
            if f.field == "document_id" and f.subject.startswith("D:") and f.value
        }
        blocks: dict[str, set[str]] = {}
        for f in record.facts:
            for e in f.evidence:
                blocks.setdefault(f.subject, set()).add(e.block.split(":", 1)[0])
        for row in rows:
            keys = sorted(blocks.get(str(row["id"]), set()))
            row["documents"] = [doc_ids.get(k, k) for k in keys]
    return rows


def _date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None


def goal_services(record: Record, policy: Policy) -> set[str]:
    services: set[str] = set()
    bases = {f.subject: f.value for f in record.facts if f.field == "basis"}
    for f in record.facts:
        if (
            f.field == "eligible_services"
            and f.value
            and (bases.get(f.subject) or "treatment_goal") in {"treatment_goal", "program_rule"}
        ):
            services |= {
                policy.service(s.strip()) or "" for s in str(f.value).split(",") if s.strip()
            }
    services.discard("")
    return services


def matches(row: dict[str, Any], c: Any, record: Record, policy: Policy) -> bool:
    if isinstance(c, AnyOf):
        return any(all(matches(row, item, record, policy) for item in conj) for conj in c.options)
    value = row.get(c.field)
    if c.op == "in":
        options = goal_services(record, policy) if c.value == "goal.services" else c.value
        if isinstance(options, str):
            raise QueryError(f"unknown set {options!r}; use (a, b) or goal.services")
        return str(value) in {str(o) for o in options}
    if isinstance(c.value, str) and c.value.lower() in {"none", "null"}:
        return bool((value is None) == (c.op == "="))
    if value is None:
        return False
    target = c.value
    if isinstance(value, date) and not isinstance(target, date):
        raise QueryError(f"{c.field} is a date; compare it with YYYY-MM-DD")
    if isinstance(value, Scenarios):
        return all(_compare(v, c.op, target) for v in value.values)
    if c.op == "contains":
        return str(target).lower() in str(value).lower()
    return _compare(value, c.op, target)


def _compare(value: Any, op: str, target: Any) -> bool:
    if isinstance(target, date) and not isinstance(value, date):
        value = _date(value)  # a date held as text compares as a date
        if value is None:
            return False
    if isinstance(target, float) and not isinstance(value, (int, float)):
        try:
            value = float(value)
        except (TypeError, ValueError):
            return False
    if not isinstance(target, (float, date)):
        value, target = str(value).lower(), str(target).lower()
    outcome: bool = {
        "=": value == target,
        "!=": value != target,
        ">": value > target,
        ">=": value >= target,
        "<": value < target,
        "<=": value <= target,
    }[op]
    return outcome


# --- execution -------------------------------------------------------------------------------


def goal_thresholds(record: Record, policy: Policy | None = None) -> list[dict[str, Any]]:
    goals = []
    for event in record.events:
        if event.kind != "goal":
            continue
        f = record.facts_of(event.id)
        # a goal whose threshold or unit the sources disagree about cannot be applied
        if (
            f.get("threshold")
            and f.get("unit")
            and f["threshold"].status != "conflicting"
            and f["unit"].status != "conflicting"
        ):
            goals.append(
                {
                    "unit": f["unit"].value,
                    "threshold": float(f["threshold"].value),
                    "comparator": f["comparator"].value if f.get("comparator") else "at_least",
                    "period": f["period"].value if f.get("period") else "week",
                    "week_start": f["week_start"].value if f.get("week_start") else None,
                    "effective": (
                        _date(f["effective_start"].value) if f.get("effective_start") else None,
                        _date(f["effective_end"].value) if f.get("effective_end") else None,
                    ),
                    "basis": f["basis"].value if f.get("basis") else None,
                    "services": {
                        policy.service(x.strip()) or ""
                        for x in str(f["eligible_services"].value).split(",")
                        if x.strip()
                    }
                    if policy and f.get("eligible_services")
                    else set(),
                    "facts": [x.id for x in f.values()],
                    "recorded": max((x.recorded_time or "" for x in f.values()), default=""),
                }
            )
    if policy is None or policy.data.get("goals", {}).get("later_supersedes", True):
        supersede_goals(goals)
    return [g for g in goals if not g.get("superseded")]


def supersede_goals(goals: list[dict[str, Any]]) -> None:
    """A later-recorded goal for the same unit and period replaces an earlier one from its own
    effective start (policy [goals] later_supersedes). The earlier goal keeps the dates before;
    one that starts on or after the later goal's start is replaced entirely. Goals whose record
    times are unknown or equal both stay (they are judged together)."""
    for later in sorted(goals, key=lambda g: g["recorded"]):
        for earlier in goals:
            if (
                earlier is later
                or earlier.get("superseded")
                or (earlier["unit"], earlier["period"]) != (later["unit"], later["period"])
                or not earlier["recorded"]
                or not later["recorded"]
                or earlier["recorded"] >= later["recorded"]
            ):
                continue
            (es, ee), (ls, _le) = earlier["effective"], later["effective"]
            if ls and es and es < ls:
                cut = ls - timedelta(days=1)
                if ee is None or ee > cut:
                    earlier["effective"] = (es, cut)
                    earlier["superseded_from"] = ls.isoformat()
                    earlier["superseded_by"] = later["facts"]
            else:
                earlier["superseded"] = True


def week_start_day(record: Record, key: str) -> int:
    m = re.match(r"week\((\w+)\)", key)
    if m and m.group(1) in WEEKDAYS:
        return WEEKDAYS.index(m.group(1))
    for g in goal_thresholds(record):
        if g["week_start"] in WEEKDAYS:
            return WEEKDAYS.index(g["week_start"])
    return 0


def group_key(row: dict[str, Any], key: str, record: Record) -> Any:
    if key.startswith("week"):
        day = row.get("date")
        if not day:
            return None
        start = week_start_day(record, key)
        begin = day - timedelta(days=(day.weekday() - start) % 7)
        return (begin, begin + timedelta(days=6))
    if key == "month":
        return row["date"].strftime("%Y-%m") if row.get("date") else None
    return row.get(key)


def execute(query: Query, record: Record, policy: Policy, result_id: str = "R1") -> dict[str, Any]:
    rows = rows_for(query.source, record)
    window = [c for c in query.where if isinstance(c, Condition) and c.field == "date"]
    others = [c for c in query.where if c not in window]
    in_window = [r for r in rows if all(matches(r, c, record, policy) for c in window)]
    selected, excluded = [], []
    for r in in_window:
        failed = next((c for c in others if not matches(r, c, record, policy)), None)
        if failed is None:
            selected.append(r)
        else:
            excluded.append(
                {
                    "id": r["id"],
                    "date": _fmt(r.get("date")),
                    "because": (
                        f"none of {failed} holds"
                        if isinstance(failed, AnyOf)
                        else f"{failed.field} {failed.op} {failed.value!r} is false ({failed.field} = {_fmt(r.get(failed.field))})"
                    ),
                    "facts": r["_facts"],
                }
            )
    groups: dict[Any, list[dict[str, Any]]] = {}
    implicit = _implicit_group(query)
    if implicit:
        # SQL semantics: a plain field selected beside an aggregate is what the rows are grouped by
        query = Query(query.source, query.where, implicit, query.select, query.text)
    if query.group_by:
        for r in selected:
            groups.setdefault(group_key(r, query.group_by, record), []).append(r)
        if query.group_by.startswith("week"):
            groups = _fill_weeks(groups, window, record, query.group_by)
    else:
        groups = {"all": selected}
    bounds = _window_bounds(window)
    result_rows = []
    collapsed = False
    for n, (key, members) in enumerate(sorted(groups.items(), key=lambda kv: _sort_key(kv[0]))):
        row: dict[str, Any] = {
            "id": f"{result_id}.{n + 1}",
            "group": _fmt(key),
            "members": [m["id"] for m in members],
            "facts": sorted({f for m in members for f in m["_facts"]}),
        }
        if query.group_by and query.group_by.startswith("week") and key:
            covered_start = max(key[0], bounds[0]) if bounds[0] else key[0]
            covered_end = min(key[1], bounds[1]) if bounds[1] else key[1]
            row["partial_week"] = (covered_start, covered_end) != key
            row["covered"] = f"{covered_start.isoformat()}..{covered_end.isoformat()}"
        for agg in query.select:
            context = {
                "week": key if query.group_by and query.group_by.startswith("week") else None,
                "window": bounds,
            }
            value = aggregate(agg, members, record, policy, row, context)
            if isinstance(value, Scenarios):
                collapsed = collapsed or value.collapsed
                value = _fmt(value)
            row[agg.label()] = value
        result_rows.append(row)
    overall = [a for a in query.select if a.name in OVERALL]
    if query.group_by and overall and len(groups) > 1:
        # the same aggregates over every selected row: totals across groups are computed by code,
        # never by the writer (distinct days across groups is not the sum of per-group counts)
        row = {
            "id": f"{result_id}.all",
            "group": "all groups",
            "groups": sum(1 for members in groups.values() if members),  # non-empty groups
            "members": [m["id"] for m in selected],
            "facts": sorted({f for m in selected for f in m["_facts"]}),
        }
        for agg in overall:
            value = aggregate(agg, selected, record, policy, row, {"week": None, "window": bounds})
            if isinstance(value, Scenarios):
                collapsed = collapsed or value.collapsed
                value = _fmt(value)
            row[agg.label()] = value
        result_rows.append(row)
    return {
        "id": result_id,
        "query": query.text,
        "source": query.source,
        **({"implicit_group_by": implicit} if implicit else {}),
        "rows": result_rows,
        "excluded": excluded,
        "scenarios_are_range_endpoints": collapsed,
    }


OVERALL = {"count", "count_distinct", "sum", "max", "min"}
# aggregates that compare rows across the whole set in order; splitting the set into groups by
# a plain field would leave each group one row ("only one PHQ-9"), so they never group implicitly
ORDERED = {"change", "percent_change", "first", "last", "days_between"}


def _implicit_group(query: Query) -> str | None:
    """SQL semantics for counts and sums: a plain field beside them groups the rows. Beside an
    order-based aggregate, a plain field is only carried along (its values over the set)."""
    if query.group_by or any(a.name in ORDERED for a in query.select):
        return None
    plain = [a.args[0] for a in query.select if a.name == "values" and a.args]
    scalar = [a for a in query.select if a.name in OVERALL]
    candidates = [f for f in plain if f not in {"id", "members", "facts"}]
    return candidates[0] if scalar and len(candidates) == 1 else None


def _sort_key(key: Any) -> tuple[int, str]:
    if isinstance(key, tuple) and key and isinstance(key[0], date):
        return (0, key[0].isoformat())
    if isinstance(key, date):
        return (0, key.isoformat())
    return (1, str(key))


def _service_in(service: Any, services: set[str]) -> bool:
    """A service in the set; a service the sources disagree about (a list) counts only when every
    possibility is in the set."""
    if isinstance(service, list):
        return bool(service) and all(x in services for x in service)
    return service in services


def _window_bounds(window: list[Condition]) -> tuple[date | None, date | None]:
    """The first and last day a date window admits (a strict bound excludes its own day)."""
    day = timedelta(days=1)
    lo = max(
        (
            c.value + day if c.op == ">" else c.value
            for c in window
            if c.op in {">=", ">", "="} and isinstance(c.value, date)
        ),
        default=None,
    )
    hi = min(
        (
            c.value - day if c.op == "<" else c.value
            for c in window
            if c.op in {"<=", "<", "="} and isinstance(c.value, date)
        ),
        default=None,
    )
    return lo, hi


def _fill_weeks(
    groups: dict[Any, list[dict[str, Any]]], window: list[Condition], record: Record, key: str
) -> dict[Any, list[dict[str, Any]]]:
    """Weeks with no rows still appear (zero counts), across the queried window."""
    lo, hi = _window_bounds(window)
    if not (lo and hi):
        return groups
    start = week_start_day(record, key)
    begin = lo - timedelta(days=(lo.weekday() - start) % 7)
    while begin <= hi:
        groups.setdefault((begin, begin + timedelta(days=6)), [])
        begin += timedelta(days=7)
    return groups


def _fmt(value: Any) -> Any:
    if isinstance(value, Scenarios):
        return (
            value.values[0]
            if len(value.values) == 1
            else {
                "scenarios": value.values,
                **({"range_endpoints": True} if value.collapsed else {}),
            }
        )
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, tuple):
        return "..".join(_fmt(v) for v in value)
    return value


def aggregate(
    agg: Aggregate,
    members: list[dict[str, Any]],
    record: Record,
    policy: Policy,
    row: dict[str, Any],
    context: dict[str, Any] | None = None,
) -> Any:
    name, args = agg.name, agg.args
    field_name = args[0] if args else None
    limit = policy.max_scenarios
    ordered = sorted(members, key=lambda m: (m.get("date") or date.min, m["id"]))

    def numeric(m: dict[str, Any]) -> Scenarios | None:
        v = m.get(field_name) if field_name else None
        if isinstance(v, Scenarios):
            return v
        try:
            return Scenarios([float(v)]) if v is not None else None
        except (TypeError, ValueError):
            raise QueryError(f"{field_name} is not numeric") from None

    if name == "count":
        return len(members)
    if name == "values" and field_name:
        found = sorted(
            {str(_fmt(m.get(field_name))) for m in members if m.get(field_name) is not None}
        )
        return found[0] if len(found) == 1 else found
    if name == "count_distinct" and field_name:
        return len({str(m.get(field_name)) for m in members if m.get(field_name) is not None})
    if name == "rows":
        return [{k: _fmt(v) for k, v in m.items() if not k.startswith("_")} for m in ordered]
    if name == "list":
        return [{k: _fmt(m.get(k)) for k in (args or ["id"])} for m in ordered]
    if name == "sum":
        total = Scenarios([0.0])
        missing = []
        for m in members:
            v = numeric(m)
            if v is None:
                missing.append(m["id"])
                continue
            total = combine(total, v, limit)
        if missing:
            row[f"missing({field_name})"] = missing
        return total
    if name in {"min", "max"}:
        values = [v for m in members if (v := numeric(m))]
        if not values:
            return None
        # the values the minimum/maximum can take across scenarios
        if name == "max":
            floor = max(min(v.values) for v in values)
            return Scenarios([x for v in values for x in v.values if x >= floor])
        ceiling = min(max(v.values) for v in values)
        return Scenarios([x for v in values for x in v.values if x <= ceiling])
    if name in {"first", "last"}:
        if not ordered:
            return None
        chosen = ordered[0] if name == "first" else ordered[-1]
        return {
            "id": chosen["id"],
            "date": _fmt(chosen.get("date")),
            field_name or "value": _fmt(chosen.get(field_name)) if field_name else None,
        }
    if name in {"change", "percent_change"}:
        kinds = {
            (str(m.get("instrument") or "").lower(), str(m.get("item") or ""))
            for m in members
            if "instrument" in m
        }
        if len(kinds) > 1:
            raise QueryError(
                f"{name}() compares different measures {sorted(kinds)}; filter to one instrument and "
                "item (item = none for total scores)"
            )
        pairs: list[tuple[dict[str, Any], Scenarios]] = [
            (m, v) for m in ordered if (v := numeric(m)) is not None
        ]
        if len(pairs) < 2:
            return {"error": "needs two values"}
        (first, a), (last, b) = pairs[0], pairs[-1]
        changes = sorted({y - x for x in a.values for y in b.values})
        out: dict[str, Any] = {
            "from": {"id": first["id"], "date": _fmt(first.get("date")), "value": _fmt(a)},
            "to": {"id": last["id"], "date": _fmt(last.get("date")), "value": _fmt(b)},
        }
        if name == "change":
            out["change"] = changes[0] if len(changes) == 1 else {"scenarios": changes}
        else:
            pct = sorted({round(100 * (y - x) / x, 1) for x in a.values for y in b.values if x})
            out["percent_change"] = pct[0] if len(pct) == 1 else {"scenarios": pct}
            out["denominator"] = _fmt(a)  # the earlier (baseline) value
        return out
    if name == "days_between":
        dated = [m for m in ordered if m.get("date")]
        if len(dated) < 2:
            return None
        return (dated[-1]["date"] - dated[0]["date"]).days
    if name == "goal_met":
        return goal_status(record, policy, context or {})
    raise QueryError(f"unsupported function {name}")


def goal_status(record: Record, policy: Policy, context: dict[str, Any]) -> dict[str, Any]:
    """Evaluate each weekly goal with its own filters, independent of the query's where clause:
    attended encounters of the services the goal counts, on days inside the week, the queried
    window and the goal's effective dates. A week only partly covered cannot be judged not met
    for an at-least goal (or met for an at-most goal); it is cannot_determine."""
    week = context.get("week")
    if not week:
        raise QueryError("goal_met() needs group_by week")
    lo, hi = context.get("window") or (None, None)
    # authorizations and payer limits are not goals the care is judged against
    goals = [
        g
        for g in goal_thresholds(record, policy)
        if g["period"] == "week" and g.get("basis") in {None, "treatment_goal", "program_rule"}
    ]
    if not goals:
        return {"status": "no_goal"}
    encounters = rows_for("encounters", record)
    checks, outcomes = [], set()
    for g in goals:
        es, ee = g["effective"]
        start = max(d for d in (week[0], lo, es) if d)
        end = min(d for d in (week[1], hi, ee) if d)
        if start > end:
            checks.append({"unit": g["unit"], "outcome": "not_applicable", "facts": g["facts"]})
            continue
        in_scope = [
            r
            for r in encounters
            if r.get("date")
            and start <= r["date"] <= end
            and (not g["services"] or _service_in(r.get("service"), g["services"]))
        ]
        counted = [r for r in in_scope if r.get("attendance") == "attended"]
        # attendance the sources disagree about is a scenario (attended or not), never dropped:
        # a goal that depends on it cannot be judged met or not met
        maybe = [
            r
            for r in in_scope
            if isinstance(r.get("attendance"), list) and "attended" in r["attendance"]
        ]
        unknown = [r["id"] for r in counted if r.get("minutes") is None]
        if g["unit"] == "days":
            sure_days = {r["date"] for r in counted}
            measured = sorted(
                {float(len(sure_days)), float(len(sure_days | {r["date"] for r in maybe}))}
            )
        elif g["unit"] == "minutes":
            total = Scenarios([0.0])
            for r in counted:
                if r.get("minutes") is not None:
                    total = combine(total, r["minutes"], 10_000)
            for r in maybe:
                extra = r["minutes"] if r.get("minutes") is not None else Scenarios([0.0])
                total = combine(total, Scenarios([0.0, *extra.values]), 10_000)
            measured = total.values
        else:
            measured = sorted({float(len(counted)), float(len(counted) + len(maybe))})
        ok = [_meets(v, g["comparator"], g["threshold"]) for v in measured]
        outcome = "met" if all(ok) else "not_met" if not any(ok) else "cannot_determine"
        if g["unit"] == "minutes" and unknown and outcome != "met":
            outcome = "cannot_determine"
        partial = (start, end) != week
        if partial and (
            (g["comparator"] == "at_least" and outcome != "met")
            or (g["comparator"] == "at_most" and outcome != "not_met")
        ):
            outcome = "cannot_determine"
        outcomes.add(outcome)
        checks.append(
            {
                "unit": g["unit"],
                "threshold": g["threshold"],
                "comparator": g["comparator"],
                "measured": measured if len(measured) > 1 else measured[0],
                "outcome": outcome,
                "covered": f"{start.isoformat()}..{end.isoformat()}",
                "partial_week": partial,
                "counted": [r["id"] for r in counted],
                **({"attendance_uncertain": [r["id"] for r in maybe]} if maybe else {}),
                "facts": g["facts"],
            }
        )
    status = (
        "not_met"
        if "not_met" in outcomes
        else "cannot_determine"
        if "cannot_determine" in outcomes
        else "met"
        if "met" in outcomes
        else "not_applicable"
    )
    # per-threshold outcomes first: a week can meet its days threshold while its minutes are
    # unresolved, and the overall status alone would hide that
    by_threshold = [
        {
            "threshold": f"{c['comparator'].replace('_', ' ')} {c['threshold']:g} {c['unit']}",
            "measured": c["measured"],
            "outcome": c["outcome"],
        }
        for c in checks
        if c["outcome"] != "not_applicable"
    ]
    return {
        "by_threshold": by_threshold,
        "overall": status,
        "status": status,
        "checks": checks,
    }


def _meets(value: float, comparator: str, threshold: float) -> bool:
    return (
        value >= threshold
        if comparator == "at_least"
        else value <= threshold
        if comparator == "at_most"
        else value == threshold
    )
