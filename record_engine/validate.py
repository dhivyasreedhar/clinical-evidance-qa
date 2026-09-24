"""③ Validate and sweep (code).

Validation: every quote must appear in its block and every typed value must appear inside its
quote. A duration therefore cannot be produced by subtraction, and a date must be stated. Invalid
fields are dropped and reported (a field name the observation kind does not have is dropped
silently); the rest of the observation is kept.

Recall sweep: every time, date, duration, identifier and score in a document must be covered by
some observation's quote. Uncovered mentions get one targeted re-extraction; anything still
uncovered becomes an open item, so extraction recall is measured rather than hoped for.
"""

from __future__ import annotations

import re
from datetime import date
from typing import Any

from record_engine.ingest import Document
from record_engine.model import Grounded, Observation, OpenItem, Recorded, Relation
from record_engine.policy import Policy
from record_engine.values import (
    dates_in,
    durations_in,
    mentions,
    numbers_in,
    parse_date,
    parse_time,
    times_in,
)

DASHES = str.maketrans(
    {"–": "-", "—": "-", "‑": "-", "−": "-", "’": "'", "‘": "'", "“": '"', "”": '"'}
)


def locate(quote: str, block_text: str) -> tuple[int, int] | None:
    """Character span of the quote in the block, ignoring whitespace and dash variants."""
    if not quote.strip():
        return None
    index = block_text.find(quote)
    if index >= 0:
        return index, index + len(quote)
    # whitespace/dash-insensitive search, mapped back to the original offsets
    source = block_text.translate(DASHES)
    parts = [re.escape(p) for p in quote.translate(DASHES).split()]
    m = re.search(r"\s+".join(parts), source)
    return m.span() if m else None


def document_years(document: Document) -> tuple[date | None, date | None]:
    """Date range of the document's most common year (so a birth date does not widen it); the
    anchor for resolving dates written without a year."""
    found = [d for d in dates_in("\n".join(document.lines)) if d.year > 1900]
    if not found:
        return None, None
    years = [d.year for d in found]
    common = max(set(years), key=years.count)
    cluster = sorted(d for d in found if abs(d.year - common) <= 1)
    return cluster[0], cluster[-1]


def check_value(
    kind_type: dict[str, Any], value: str, quote: str, anchors: tuple[date | None, date | None]
) -> str | None:
    """None when the typed value is well-formed and stated by its quote; else the reason."""
    typ = kind_type.get("type", "text")
    if typ == "date":
        parsed = parse_date(value)
        if parsed is None:
            return "date_not_iso"
        if parsed not in dates_in(quote, *anchors):
            return "date_not_in_quote"
    elif typ == "time":
        parsed_time = parse_time(value)
        if parsed_time is None or len(value.strip()) > 8:
            return "time_not_hh_mm"
        if parsed_time not in times_in(quote):
            return "time_not_in_quote"
    elif typ == "minutes":
        try:
            number = float(value)
        except ValueError:
            return "minutes_not_a_number"
        if number not in durations_in(quote) and number not in numbers_in(quote):
            return "duration_not_stated_in_quote"
    elif typ == "number":
        try:
            number = float(value)
        except ValueError:
            return "not_a_number"
        if number not in numbers_in(quote):
            return "number_not_in_quote"
    elif typ == "enum":
        if value not in kind_type.get("values", []):
            return "value_not_in_enum"
    elif typ == "bool":
        if value not in {"yes", "no"}:
            return "bool_not_yes_no"
    return None


def validate(
    document: Document, raw: list[dict[str, Any]], policy: Policy
) -> tuple[list[Observation], list[OpenItem]]:
    blocks = {b.id: b.text for b in document.blocks}
    anchors = document_years(document)
    observations: list[Observation] = []
    problems: list[OpenItem] = []

    def bad(block: str | None, text: str) -> None:
        problems.append(
            OpenItem(
                kind="invalid", subject=document.key, text=text, blocks=[block] if block else []
            )
        )

    for item in raw:
        kind = item.get("kind")
        types = policy.field_types(kind or "")
        if not types:
            bad(None, f"unknown observation kind {kind!r}")
            continue
        fields: list[Grounded] = []
        # A field given without its own block (typically a classification such as a finding's
        # type) is grounded in the observation's first quoted field; typed values must still
        # appear in that quote.
        anchor = next(
            (
                (f.get("block"), f.get("quote", ""))
                for f in item["fields"]
                if f.get("block") in blocks and f.get("quote")
            ),
            None,
        )
        for f in item["fields"]:
            name, value, quote, block = (
                f.get("name"),
                str(f.get("value", "")).strip(),
                f.get("quote", ""),
                f.get("block"),
            )
            if (block not in blocks or not quote) and anchor:
                block, quote = anchor
            if name not in types or value == "":
                continue
            if block not in blocks:
                bad(block, f"{kind}.{name}: block {block} does not exist")
                continue
            if locate(quote, blocks[block]) is None:
                bad(block, f"{kind}.{name}: quote not found in block: {quote!r}")
                continue
            reason = check_value(types[name], value, quote, anchors)
            if reason:
                bad(block, f"{kind}.{name}={value!r}: {reason} ({quote!r})")
                continue
            if types[name].get("type") == "time":
                value = parse_time(value) or value
            fields.append(Grounded(name=name, value=value, quote=quote, block=block))
        if not fields:
            continue
        recorded = []
        for r in item.get("recorded", []):
            block = r.get("block")
            parsed = parse_date(str(r.get("value", "")))
            if (
                block in blocks
                and locate(r.get("quote", ""), blocks[block])
                and parsed
                and (parsed in dates_in(r.get("quote", ""), *anchors))
            ):
                recorded.append(Recorded(**{k: r[k] for k in ("role", "value", "quote", "block")}))
            else:
                bad(block, f"recorded {r.get('role')}={r.get('value')!r} not stated in its quote")
        relation_data = item.get("relation") or {"type": "none"}
        relation = Relation(
            type=relation_data.get("type", "none"),
            target_desc=relation_data.get("target_desc"),
            fields=list(relation_data.get("fields") or []),
            quote=relation_data.get("quote"),
            block=relation_data.get("block"),
        )
        if relation.type != "none" and not (
            relation.block in blocks
            and relation.quote
            and locate(relation.quote, blocks[relation.block])
        ):
            bad(relation.block, f"relation {relation.type} is not stated in the cited quote")
            relation = Relation()
        observations.append(
            Observation(
                id=item["id"],
                doc=document.key,
                kind=kind,
                fields=fields,
                evidence_kind=item.get("evidence_kind", "actual"),
                attestation=item.get("attestation", "unknown"),
                recorded=recorded,
                relation=relation,
                source=item.get("source", "extract"),
            )
        )
    return observations, problems


def covered_spans(
    document: Document, observations: list[Observation]
) -> dict[str, list[tuple[int, int]]]:
    blocks = {b.id: b.text for b in document.blocks}
    spans: dict[str, list[tuple[int, int]]] = {}
    for o in observations:
        quotes = [(f.block, f.quote) for f in o.fields] + [(r.block, r.quote) for r in o.recorded]
        if o.relation.block and o.relation.quote:
            quotes.append((o.relation.block, o.relation.quote))
        for block, quote in quotes:
            if block in blocks and (span := locate(quote, blocks[block])):
                spans.setdefault(block, []).append(span)
    return spans


def uncovered(
    document: Document,
    observations: list[Observation],
    dismissed: set[tuple[str, str]] | None = None,
) -> list[tuple[str, str, str]]:
    """(block, mention kind, mention text) for mentions no quote covers."""
    spans = covered_spans(document, observations)
    dismissed = dismissed or set()
    missing = []
    for block in document.blocks:
        for kind, text, start, end in mentions(block.text):
            if (block.id, text) in dismissed:
                continue
            if not any(s < end and start < e for s, e in spans.get(block.id, [])):
                missing.append((block.id, kind, text))
    # one entry per (block, text)
    return list(dict.fromkeys(missing))
