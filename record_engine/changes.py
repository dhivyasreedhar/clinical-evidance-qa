"""Record changes and provenance: diff two records, trace a fact to its sources."""

from __future__ import annotations

from typing import Any

from record_engine.ingest import Document
from record_engine.model import Fact, Observation, Record


def _key(f: Fact) -> tuple[str, str]:
    return (f.subject, f.field)


def _shown(f: Fact) -> str:
    value = " or ".join(map(str, f.scenarios)) if f.status == "conflicting" else str(f.value)
    return f"{value} ({f.status}, {f.rule})"


def diff(before: Record, after: Record) -> dict[str, Any]:
    """What changed between two builds: documents, events, facts (value, status or rule) and
    open items. Facts are matched by (subject, field)."""
    old = {_key(f): f for f in before.facts}
    new = {_key(f): f for f in after.facts}
    changed = []
    for k in sorted(old.keys() & new.keys()):
        a, b = old[k], new[k]
        if (a.value, a.scenarios, a.status, a.rule) != (b.value, b.scenarios, b.status, b.rule):
            changed.append(
                {"subject": k[0], "field": k[1], "before": _shown(a), "after": _shown(b)}
            )
    docs_before = {d["key"] for d in before.documents}
    docs_after = {d["key"] for d in after.documents}
    items_before = {(o.kind, o.text) for o in before.open_items}
    items_after = {(o.kind, o.text) for o in after.open_items}
    return {
        "documents_added": sorted(docs_after - docs_before),
        "documents_removed": sorted(docs_before - docs_after),
        "events_added": sorted({e.id for e in after.events} - {e.id for e in before.events}),
        "events_removed": sorted({e.id for e in before.events} - {e.id for e in after.events}),
        "facts_added": [
            {"subject": k[0], "field": k[1], "value": _shown(new[k])}
            for k in sorted(new.keys() - old.keys())
        ],
        "facts_removed": [
            {"subject": k[0], "field": k[1], "value": _shown(old[k])}
            for k in sorted(old.keys() - new.keys())
        ],
        "facts_changed": changed,
        "open_items_added": sorted(t for _, t in items_after - items_before),
        "open_items_resolved": sorted(t for _, t in items_before - items_after),
    }


def diff_markdown(d: dict[str, Any]) -> str:
    out = ["# Record changes", ""]
    for key, label in [
        ("documents_added", "Documents added"),
        ("documents_removed", "Documents removed"),
        ("events_added", "Events added"),
        ("events_removed", "Events removed"),
    ]:
        if d[key]:
            out += [f"**{label}:** " + ", ".join(d[key]), ""]
    if d["facts_changed"]:
        out += ["## Facts changed", "", "| Subject | Field | Before | After |", "|---|---|---|---|"]
        out += [
            f"| {c['subject']} | {c['field']} | {c['before']} | {c['after']} |"
            for c in d["facts_changed"]
        ]
        out.append("")
    for key, label in [("facts_added", "Facts added"), ("facts_removed", "Facts removed")]:
        if d[key]:
            out += (
                [f"## {label} ({len(d[key])})", ""]
                + [f"- {x['subject']} {x['field']}: {x['value']}" for x in d[key][:80]]
                + [""]
            )
    for key, label in [
        ("open_items_added", "New open items"),
        ("open_items_resolved", "Open items resolved"),
    ]:
        if d[key]:
            out += [f"## {label}", ""] + [f"- {t}" for t in d[key]] + [""]
    if len(out) == 2:
        out.append("No changes.")
    return "\n".join(out) + "\n"


def trace(
    target: str, record: Record, observations: list[Observation], documents: list[Document]
) -> str:
    """Fact or event → facts → evidence (stance, source lines, quote) → observation provenance."""
    by_obs = {o.id: o for o in observations}
    lines_of = {d.key: d for d in documents}
    facts = [f for f in record.facts if f.id == target] or [
        f for f in record.facts if f.subject == target
    ]
    if not facts:
        return f"No fact or event {target!r} in the record."
    event = next((e for e in record.events if e.id == facts[0].subject), None)
    out = [f"# Trace: {target}", ""]
    if event:
        out += [
            f"Event {event.id} ({event.kind}), linked by {event.link.get('linked_by', '—')}; {len(event.observations)} observations",
            "",
        ]
    for f in facts:
        out += [f"## {f.subject} · {f.field} = {_shown(f)}", "", f"Rule: {f.rule}. {f.reason}", ""]
        for e in f.evidence:
            o = by_obs.get(e.observation)
            prov = (
                f"{o.kind}, {o.evidence_kind}, {o.attestation}"
                + (
                    f", recorded {', '.join(r.role + ' ' + r.value for r in o.recorded)}"
                    if o.recorded
                    else ", record time unknown"
                )
                + (
                    f", {o.relation.type} {o.relation.target_desc or ''}".rstrip()
                    if o.relation.type != "none"
                    else ""
                )
                if o
                else "observation not found"
            )
            key, lines = e.block.split(":", 1)
            name = lines_of[key].filename if key in lines_of else key
            out.append(f"- {e.stance}: {name}:{lines[1:]} “{e.quote}” — {prov}")
        out.append("")
    return "\n".join(out)
