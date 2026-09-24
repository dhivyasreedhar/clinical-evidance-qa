"""Cross-checked extraction: two independent readings of every document, compared by code.

A single extraction is one draw from the model: the same line can be read differently from run to
run (a therapist's session start taken for the patient's arrival, a department taken for another
organisation). So each document is read twice:

- reading A at temperature 0 (the primary reading);
- reading B as an independent sample.

Records are built from both, and code compares every grounded key field (dates, times, durations,
numbers, enumerated statuses, identifiers, the service category, provenance and relations) of
every event, per document. A document where the readings disagree gets one focused re-read at
temperature 0 that is told exactly what was disputed; its observations of the disputed kinds
replace reading A's for the events involved and the record is rebuilt. A disputed point is settled when the re-read agrees
with one of the two readings (two of three); otherwise it stays visible as an open item. A re-read
may add what both readings left out but may not contradict both of them; one that does is
rejected for its whole document, which keeps reading A with its disputed points open.
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

from record_engine import extract as ex
from record_engine import llm
from record_engine.ingest import Document
from record_engine.link import id_key, issuer_core
from record_engine.model import Observation, OpenItem, Record
from record_engine.pipeline import observe_all
from record_engine.policy import Policy
from record_engine.reconcile import build_record
from record_engine.validate import validate
from record_engine.values import parse_date, parse_time

KEY_TYPES = {"date", "time", "minutes", "number", "enum", "bool"}
# kinds a document states once per event (its contact record of the visit, its own header)
SINGLE_KINDS = {"contact", "doc_meta"}
# Events whose readings are compared; findings are paraphrases and are not.
COMPARED = {"patient", "document", "encounter", "measurement", "medication", "goal", "charge"}

Key = tuple[str, str]  # (event id, document key)
Values = dict[str, frozenset[str]]  # compared field -> normalised values


@dataclass
class Point:
    """One disagreement between the readings about one event in one document."""

    event: str
    doc: str
    field: str
    a: list[str]
    b: list[str]

    def text(self) -> str:
        a = ", ".join(self.a) or "not stated"
        b = ", ".join(self.b) or "not stated"
        name = self.field.split(".")[-1].replace("_", " ")
        return f"{self.event}, {name} in {self.doc}: one reading has {a}, the other {b}"


def compared_fields(policy: Policy) -> dict[str, set[str]]:
    ids = set(policy.data.get("crosscheck", {}).get("id_fields", []))
    return {
        kind: {
            f["name"]
            for f in spec["fields"]
            if f["type"] in KEY_TYPES or f["name"] in ids or f["name"] == "service"
        }
        for kind, spec in policy.kinds.items()
    }


def normalise(kind_types: dict[str, Any], name: str, value: str, policy: Policy) -> str:
    typ = kind_types.get(name, {}).get("type", "text")
    if name == "issuer":
        return issuer_core(value, set(policy.link.get("issuer_generic_words", [])))
    if name == "service":
        # compared by category; wording outside every category is free text, not compared
        known = sorted(c for c in policy.categories(value) if c in policy.services["order"])
        return " ".join(known) or "uncategorised"
    if typ == "time":
        return parse_time(value) or value
    if typ == "date":
        parsed = parse_date(value)
        return parsed.isoformat() if parsed else value
    if typ in {"minutes", "number"}:
        try:
            return f"{float(value):g}"
        except ValueError:
            return value
    if typ in {"enum", "bool"}:
        return value.strip().lower()
    return id_key(value)


def comparable(
    record: Record, observations: list[Observation], policy: Policy
) -> tuple[dict[Key, Values], dict[Key, str], dict[Key, list[Observation]]]:
    """Per (event, document): the compared values, the event's kind, and its observations."""
    by_id = {o.id: o for o in observations}
    fields = compared_fields(policy)
    values: dict[Key, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    kinds: dict[Key, str] = {}
    members: dict[Key, list[Observation]] = defaultdict(list)
    for event in record.events:
        if event.kind not in COMPARED:
            continue
        for oid in event.observations:
            o = by_id.get(oid)
            if o is None:
                continue
            key = (event.id, o.doc)
            kinds[key] = event.kind
            members[key].append(o)
            types = policy.field_types(o.kind)
            seen = values[key]
            for f in o.fields:
                if f.name in fields.get(o.kind, set()):
                    seen[f"{o.kind}.{f.name}"].add(normalise(types, f.name, f.value, policy))
            seen[f"{o.kind}.evidence_kind"].add(o.evidence_kind)
            seen[f"{o.kind}.attestation"].add(o.attestation)
            if o.relation.type != "none":
                seen[f"{o.kind}.relation"].add(o.relation.type)
    frozen = {k: {f: frozenset(v) for f, v in fs.items()} for k, fs in values.items()}
    return frozen, kinds, members


def disagreements(
    a: dict[Key, Values], b: dict[Key, Values], kinds_a: dict[Key, str], kinds_b: dict[Key, str]
) -> list[Point]:
    """Every compared field that differs between the readings. An event one reading has and the
    other does not is paired, per document and kind, with the other's unmatched event (the same
    contact read with another date or number); what is left unpaired is itself a disagreement."""
    points: list[Point] = []

    def differ(event: str, doc: str, va: Values, vb: Values) -> None:
        for name in sorted(set(va) | set(vb)):
            left, right = va.get(name, frozenset()), vb.get(name, frozenset())
            if left != right:
                points.append(Point(event, doc, name, sorted(left), sorted(right)))

    for key in sorted(set(a) & set(b)):
        differ(key[0], key[1], a[key], b[key])
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    for key in only_a:
        match = next(
            (k for k in only_b if k[1] == key[1] and kinds_b.get(k) == kinds_a.get(key)), None
        )
        if match is None:
            points.append(Point(key[0], key[1], "event", ["recorded"], ["not recorded"]))
            continue
        only_b.remove(match)
        points.append(Point(key[0], key[1], "event", [key[0]], [match[0]]))
        differ(key[0], key[1], a[key], b[match])
    for key in only_b:
        points.append(Point(key[0], key[1], "event", ["not recorded"], ["recorded"]))
    return points


REREAD = """Two independent readings of this document disagree on the points listed below. Re-read
the document carefully and return, under the same rules, complete observations (every field the
document states, not only the disputed ones) for each contact or item the points concern. Decide
each point from the document's own words: which value the document states for that field, or that
it does not state one. Return nothing else."""


def disputed_kinds(points: list[Point]) -> set[str]:
    """The observation kinds a document's re-read replaces: those the disputed fields belong to;
    every compared kind when the readings disagree about which events the document records."""
    if any(p.field == "event" for p in points):
        return {
            "doc_meta",
            "contact",
            "interval",
            "measurement",
            "medication",
            "plan_goal",
            "charge",
        }
    return {p.field.split(".")[0] for p in points}


def reread(
    document: Document, policy: Policy, points: list[Point], quotes: list[str]
) -> list[Observation]:
    listing = "\n".join(f"- {p.text()}" for p in points)
    shown = "\n".join(f"  {q}" for q in quotes[:40])
    user = (
        f"Document: {document.filename}\n\nBlocks:\n{ex.document_text(document)}\n\n"
        f"Disputed points:\n{listing}\n\nWhat each reading quoted for these items:\n{shown}\n\n"
        + REREAD
    )
    output = llm.call(
        f"reread:{document.key}",
        ex.system_prompt(policy),
        user,
        ex.schema(policy),
        llm.WRITER,
    )
    observations, _problems = validate(document, ex.to_raw(document, output, "sweep"), policy)
    # findings are paraphrases and not compared
    kept = [o for o in observations if o.kind != "finding"]
    for o in kept:
        o.id = f"{o.id}~reread"
    return kept


def reading(
    documents: list[Document], policy: Policy, workers: int, trial: str, temperature: float
) -> tuple[list[Observation], list[OpenItem], list[dict[str, Any]]]:
    with llm.sampling(temperature, trial):
        observations, problems, stats = observe_all(documents, policy, workers)
    if trial:
        suffix = "~" + trial.replace("/", "~")
        for o in observations:
            o.id += suffix
    return observations, problems, stats


def observe_checked(
    documents: list[Document], policy: Policy, workers: int = 6
) -> tuple[list[Observation], list[OpenItem], dict[str, Any]]:
    """Observations cross-checked between two readings, with disagreements settled by a focused
    re-read or left open. Returns observations, open items and the cross-check report."""
    obs_a, problems_a, stats_a = reading(documents, policy, workers, "", 0.0)
    obs_b, problems_b, _ = reading(documents, policy, workers, "reading-b", 1.0)
    record_a = build_record(documents, obs_a, policy, problems_a)
    record_b = build_record(documents, obs_b, policy, problems_b)
    values_a, kinds_a, members_a = comparable(record_a, obs_a, policy)
    values_b, kinds_b, members_b = comparable(record_b, obs_b, policy)
    points = disagreements(values_a, values_b, kinds_a, kinds_b)

    by_doc: dict[str, list[Point]] = defaultdict(list)
    for p in points:
        by_doc[p.doc].append(p)
    documents_by_key = {d.key: d for d in documents}

    def settle(doc: str) -> tuple[str, list[Observation], set[str]]:
        doc_points = by_doc[doc]
        events = {p.event for p in doc_points}
        kinds = disputed_kinds(doc_points)
        replaced = {
            o.id
            for (e, d), os in members_a.items()
            if d == doc and e in events
            for o in os
            if o.kind in kinds
        }
        quotes = [
            f"{o.kind}.{f.name} = {f.value!r} ({f.quote!r})"
            for members in (members_a, members_b)
            for (e, d), os in members.items()
            if d == doc and e in events
            for o in os
            for f in o.fields
        ]
        found = reread(documents_by_key[doc], policy, doc_points, sorted(set(quotes)))
        return doc, [o for o in found if o.kind in kinds], replaced

    with ThreadPoolExecutor(workers) as pool:
        settled = list(pool.map(llm.carry(settle), sorted(by_doc)))

    def combine(accepted: set[str]) -> list[Observation]:
        removed = {oid for doc, _, ids in settled if doc in accepted for oid in ids}
        return [o for o in obs_a if o.id not in removed] + [
            o for doc, reread_obs, _ in settled if doc in accepted for o in reread_obs
        ]

    # A re-read arbitrates between the readings: it may not contradict both of them (for example
    # attach a phone call about a session to the session itself, where both readings kept them
    # apart). It may add what both readings left out. A document whose re-read contradicts both
    # keeps reading A, and its disputed points stay open.
    accepted = set(by_doc)
    observations = combine(accepted)
    record_c = build_record(documents, observations, policy, problems_a)
    values_c, kinds_c, _ = comparable(record_c, observations, policy)
    against_a = disagreements(values_c, values_a, kinds_c, kinds_a)
    against_b = disagreements(values_c, values_b, kinds_c, kinds_b)

    def contradicted(found: list[Point]) -> dict[tuple[str, str, str], bool]:
        """(doc, event, field) where the rebuilt record differs from a reading, mapped to whether
        it contradicts that reading. Dropping an event the reading has contradicts it; adding one
        the reading lacks does not. A document states one contact per event and one header, so
        for those any other value contradicts; segments, measurements and other repeatable items
        can be added to, so there only dropping a reading's value contradicts it. An addition to a
        silent reading never does."""
        out = {}
        for p in found:
            if p.doc not in accepted:
                continue
            kind = p.field.split(".")[0]
            if p.field == "event":
                # p.a is the rebuilt record's side: "recorded" there is an addition
                out[(p.doc, p.event, p.field)] = p.a != ["recorded"]
            elif kind in SINGLE_KINDS:
                out[(p.doc, p.event, p.field)] = bool(p.b)
            else:
                out[(p.doc, p.event, p.field)] = not set(p.b) <= set(p.a)
        return out

    diff_a, diff_b = contradicted(against_a), contradicted(against_b)
    # a value that differs from both readings, where at least one of them stated something
    invented = {k for k in set(diff_a) & set(diff_b) if diff_a[k] or diff_b[k]}
    rejected = sorted({doc for doc, _, _ in invented})
    if rejected:
        accepted -= set(rejected)
        observations = combine(accepted)
        record_c = build_record(documents, observations, policy, problems_a)
        values_c, kinds_c, _ = comparable(record_c, observations, policy)

    # two of three: a point is settled when the re-read agrees with one of the readings
    open_items: list[OpenItem] = []
    report_points = []
    for p in points:
        outcome = "settled" if p.doc in accepted and agrees(p, values_c) else "open"
        report_points.append({**p.__dict__, "outcome": outcome})
        if outcome == "open":
            open_items.append(
                OpenItem(
                    kind="reading_disagreement",
                    subject=p.event,
                    text=(
                        f"Two readings of the document disagree ({p.text()}), and a focused "
                        "re-read did not settle it; the record uses "
                        + ("the re-read." if p.doc in accepted else "the first reading.")
                    ),
                    blocks=sorted(
                        {f.block for o in members_a.get((p.event, p.doc), []) for f in o.fields}
                    ),
                )
            )
    report = {
        "documents": len(documents),
        "disagreements": len(points),
        "documents_reread": len(by_doc),
        "rereads_rejected": [
            {"doc": d, "invented": sorted(f"{e} {f}" for doc, e, f in invented if doc == d)}
            for d in rejected
        ],
        "settled": sum(r["outcome"] == "settled" for r in report_points),
        "open": sum(r["outcome"] == "open" for r in report_points),
        "points": report_points,
        "per_document": stats_a,
    }
    return observations, problems_a + open_items, report


def agrees(point: Point, values: dict[Key, Values]) -> bool:
    """Whether the rebuilt record settles the point with one of the two readings' answers. Whether
    an event exists always takes one reading's side; a contact the readings identified
    differently is settled when the rebuilt record has it under either identity."""
    if point.field == "event":
        if "recorded" in point.a + point.b:
            return True
        return any(d == point.doc and e in point.a + point.b for e, d in values)
    current = values.get((point.event, point.doc), {}).get(point.field, frozenset())
    return sorted(current) in (point.a, point.b)
