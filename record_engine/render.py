"""Readable outputs: abstraction.md (what reviewers read) and answers.md."""

from __future__ import annotations

import re
from typing import Any

from record_engine.dates import find_dates
from record_engine.ingest import Document
from record_engine.model import Fact, Record
from record_engine.query import REFERENCE_DISPOSITIONS

STATUS_MARK = {
    "established": "established",
    "corroborated": "corroborated",
    "documented": "documented",
    "conflicting": "**conflicting**",
    "superseded": "superseded",
    "not_documented": "**not documented**",
}


# Where Markdown outputs find the source documents; the command line sets it from --out.
DOCUMENTS_BASE = "../documents"


def source_link(block: str, documents: dict[str, Document]) -> str:
    key, lines = block.split(":", 1)
    document = documents.get(key)
    name = document.filename if document else key
    return f"[{name}:{lines[1:]}]({DOCUMENTS_BASE}/{name}#{lines})"


def cell(text: Any) -> str:
    """A value safe inside a markdown table cell."""
    return str(text).replace("|", "\\|").replace("\n", " ")


def fmt(fact: Fact | None) -> str:
    if fact is None:
        return "—"
    if fact.status == "conflicting":
        return " or ".join(fmt_value(v) for v in fact.scenarios)
    if fact.status == "not_documented":
        return "not documented"
    return fmt_value(fact.value)


def fmt_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:g}"
    if isinstance(value, list):
        return "–".join(map(str, value))
    return str(value)


def sources(facts: list[Fact], documents: dict[str, Document]) -> str:
    stances = {"supports", "copy", "contradicts", "superseded"}
    blocks = sorted({e.block for f in facts for e in f.evidence if e.stance in stances})
    return ", ".join(source_link(b, documents) for b in blocks)


def encounter_rows(record: Record, references: bool = False) -> list[dict[str, Any]]:
    """Encounters, or (references=True) entries that document no visit."""
    rows = []
    for event in record.events:
        if event.kind != "encounter":
            continue
        facts = record.facts_of(event.id)
        is_reference = (
            facts.get("disposition") is not None
            and facts["disposition"].value in REFERENCE_DISPOSITIONS
        )
        if is_reference != references:
            continue
        rows.append(
            {
                "event": event,
                "facts": facts,
                "date": (facts["date"].value if "date" in facts else None) or "",
            }
        )
    return sorted(rows, key=lambda r: (str(r["date"]), r["event"].id))


def abstraction_markdown(record: Record, documents_list: list[Document]) -> str:
    documents = {d.key: d for d in documents_list}
    out = [
        "# Clinical abstraction",
        "",
        f"Engine {record.version}, policy {record.policy}. Every value below was decided by code from "
        "source-grounded observations; each row links to the source lines. Status: *documented* = one "
        "source; *corroborated* = independent sources agree; *established* = a written rule settled a "
        "disagreement; **conflicting** = sources of equal standing disagree (all values kept).",
        "",
        "## Encounters",
        "",
        "| Date | Encounter | Service | Attendance | Disposition | Creditable minutes | Status | Rule | Sources |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for row in encounter_rows(record):
        f = row["facts"]
        minutes = f.get("minutes")
        rules = sorted({x.rule for x in f.values() if x.rule not in {"single_source", "computed"}})
        worst = (
            "conflicting"
            if any(x.status == "conflicting" for x in f.values())
            else (
                minutes.status
                if minutes
                else (f.get("attendance").status if f.get("attendance") else "documented")
            )
        )
        out.append(
            "| {date} | {id} | {service} | {att} | {disp} | {mins} | {status} | {rules} | {src} |".format(
                date=row["date"],
                id=row["event"].id,
                service=fmt(f.get("service")),
                att=fmt(f.get("attendance")),
                disp=fmt(f.get("disposition")),
                mins=fmt(minutes) if minutes else "—",
                status=STATUS_MARK.get(worst, worst),
                rules=", ".join(rules) or "—",
                src=sources([x for x in f.values()], documents),
            )
        )
    out += ["", "### How each encounter was decided", ""]
    for row in encounter_rows(record):
        f = row["facts"]
        out.append(f"**{row['event'].id}** ({row['date']})")
        for name in (
            "attendance",
            "service",
            "presence_start",
            "presence_end",
            "stated_minutes",
            "minutes",
            "disposition",
        ):
            fact = f.get(name)
            if fact:
                out.append(f"- {name}: {fmt(fact)} — {fact.status}; {fact.rule}. {fact.reason}")
        for fact in [
            x for x in record.facts if x.subject == row["event"].id and x.field == "break"
        ]:
            out.append(f"- break/gap {fmt(fact)} — {fact.status}")
        out.append("")

    refs = encounter_rows(record, references=True)
    if refs:
        out += [
            "## References with no visit record",
            "",
            "Entries that mention a visit or handle the chart but document no visit of their own "
            "(a booking, template, charge, a reference to a visit recorded elsewhere, or chart "
            "handling). They are never counted.",
            "",
            "| Date | Entry | Service | Why | Sources |",
            "|---|---|---|---|---|",
        ]
        for row in refs:
            f = row["facts"]
            out.append(
                f"| {row['date']} | {cell(row['event'].id)} | {fmt(f.get('service'))} | "
                f"{cell(f['disposition'].reason)} | {sources(list(f.values()), documents)} |"
            )
        out.append("")
    out += ["## Measurements", "", "| Measure | Score | Status | Sources |", "|---|---|---|---|"]
    for event in record.events:
        if event.kind == "measurement":
            f = record.facts_of(event.id)
            out.append(
                f"| {event.id[2:]} | {fmt(f.get('score'))} | {STATUS_MARK.get(f['score'].status, '') if f.get('score') else ''} | {sources(list(f.values()), documents)} |"
            )
    out += ["", "## Goals", ""]
    for event in record.events:
        if event.kind == "goal":
            f = record.facts_of(event.id)
            out.append(
                f"- {fmt(f.get('comparator'))} {fmt(f.get('threshold'))} {fmt(f.get('unit'))} per {fmt(f.get('period'))} "
                f"(week starts {fmt(f.get('week_start'))}; counts: {fmt(f.get('eligible_services'))}) — {sources(list(f.values()), documents)}"
            )
    out += ["", "## Medications", ""]
    for event in record.events:
        if event.kind == "medication":
            f = record.facts_of(event.id)
            out.append(
                f"- {fmt(f.get('date'))}: {fmt(f.get('name'))} {fmt(f.get('dose')) if f.get('dose') else ''} {fmt(f.get('schedule')) if f.get('schedule') else ''} ({fmt(f.get('change'))}) — {sources(list(f.values()), documents)}"
            )
    out += ["", "## Open items", ""]
    labels = {
        "conflict": "Conflicts",
        "missing": "Expected but not documented",
        "candidate_link": "Possible duplicates (not merged)",
        "unextracted_mention": "Mentions not captured by extraction",
        "invalid": "Extracted values rejected by validation",
        "reading_disagreement": "Readings of a document that disagree (not settled)",
        "other_patient": "Documents about another patient (set aside)",
    }
    for kind, label in labels.items():
        items = [i for i in record.open_items if i.kind == kind]
        if not items:
            continue
        out += [f"### {label} ({len(items)})", ""]
        for item in items[:60]:
            src = ", ".join(source_link(b, documents) for b in item.blocks if ":" in b)
            out.append(f"- {item.text}" + (f" — {src}" if src else ""))
        if len(items) > 60:
            out.append(f"- … {len(items) - 60} more in abstraction.json")
        out.append("")
    out += ["## Documents", "", "| File | Title | Copy of | Observations |", "|---|---|---|---|"]
    for d in record.documents:
        out.append(
            f"| {cell(d['filename'])} | {cell(d['title'] or '')} | {d['copy_of'] or ('(contains copied content)' if d['copy_observations'] else '')} | {d['observations']} |"
        )
    return "\n".join(out) + "\n"


def _cell(value: Any) -> str:
    if isinstance(value, dict) and "scenarios" in value:
        return " or ".join(fmt_value(v) for v in value["scenarios"]) + (
            " (range ends)" if value.get("range_endpoints") else ""
        )
    if isinstance(value, dict) and "status" in value:
        return str(value["status"]).replace("_", " ") + (
            f" ({value['note']})" if value.get("note") else ""
        )
    if isinstance(value, list):
        return f"{len(value)} items"
    if isinstance(value, dict):
        return ", ".join(f"{k}: {_cell(v)}" for k, v in value.items() if k != "facts")
    return fmt_value(value) if value is not None else "—"


def result_table(result: dict[str, Any]) -> list[str]:
    rows = result["rows"]
    if not rows:
        return [f"*{result['purpose']}* — no rows (`{result['query']}`)", ""]
    columns = [k for k in rows[0] if k not in {"id", "members", "facts", "covered"}]
    lines = [
        f"*{result.get('purpose', '')}* — `{result['query']}`",
        "",
        "| " + " | ".join(columns) + " |",
        "|" + "---|" * len(columns),
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(_cell(row.get(c))) for c in columns) + " |")
    for row in rows:
        for key, value in row.items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                lines += ["", f"{key}:", ""]
                cols = list(value[0].keys())
                lines += ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
                lines += [
                    "| " + " | ".join(cell(_cell(item.get(c))) for c in cols) + " |"
                    for item in value
                ]
    if result.get("excluded"):
        lines += [
            "",
            "Not counted: "
            + "; ".join(
                f"{e['id']} ({e['date']}): {e['because']}" for e in result["excluded"][:30]
            ),
        ]
    return lines + [""]


KEY_FIELDS = (
    "attendance",
    "minutes",
    "presence_start",
    "presence_end",
    "break",
    "score",
    "text",
    "threshold",
    "name",
)


def _value_tokens(value: Any) -> set[str]:
    """Tokens that identify a fact value in prose: numbers, clock times, significant words."""
    text = " ".join(map(str, value)) if isinstance(value, list) else str(value)
    tokens = set(re.findall(r"\d{1,2}:\d{2}|\d+(?:\.\d+)?", text))
    tokens |= {w for w in re.findall(r"[a-z]{5,}", text.lower())}
    return {t[:-2] if t.endswith(".0") else t for t in tokens}


def _event_blocks(event_id: str, record: Record, text: str | None = None) -> list[str]:
    """The source lines behind an item's facts that the statement states (by value); if the
    statement states none of them, the item's key facts."""
    stated = set(re.findall(r"\d{1,2}:\d{2}|\d+(?:\.\d+)?", text or "")) | set(
        re.findall(r"[a-z]{5,}", (text or "").lower())
    )
    matching: list[str] = []
    key: list[str] = []
    for f in record.facts:
        if f.subject != event_id:
            continue
        blocks = [e.block for e in f.evidence if e.stance in {"supports", "contradicts"}]
        tokens = _value_tokens(f.values())
        if text and tokens and tokens & stated and f.field not in {"date", "records"}:
            matching += [b for b in blocks if b not in matching]
        if f.field in KEY_FIELDS or f.field.startswith("break"):
            key += [b for b in blocks if b not in key]
    return (matching or key)[:3]


STOPWORDS = set(
    "that this with from were was have been their there which when what they them than then "
    "into also only both each more most other some such very will would could should about "
    "record records document documents documented patient session sessions".split()
)
ID = re.compile(r"\b[A-Z]{1,5}-[A-Z]?\d+[A-Z]?\b")


def anchors(text: str) -> tuple[set[str], set[str]]:
    """Strong anchors (dates, clock times, record IDs, numbers) and content words of a text."""
    strong = {d.isoformat() for d in find_dates(text, expand=False)}
    strong |= set(re.findall(r"\b\d{1,2}:\d{2}\b", text))
    strong |= set(ID.findall(text))
    strong |= {
        n[:-2] if n.endswith(".0") else n
        for n in re.findall(r"(?<![\d:.-])\d+(?:\.\d+)?(?![\d:])", text)
    }
    words = {w for w in re.findall(r"[a-z]{4,}", text.lower()) if w not in STOPWORDS}
    return strong, words


def prune_blocks(
    text: str, groups: dict[str, list[str]], texts: dict[str, str], keep: set[str] | None = None
) -> dict[str, list[str]]:
    """Keep the source lines that share a date, time, record ID or number, or at least two
    content words, with the statement citing them; a statement always keeps its best line."""
    keep = keep or set()
    strong, words = anchors(text)
    scored = []
    kept: dict[str, list[str]] = {}
    for subject, blocks in groups.items():
        for b in blocks:
            b_strong, b_words = anchors(texts.get(b, ""))
            shared = len(strong & b_strong) * 3 + len(words & b_words)
            scored.append((shared, subject, b))
            if subject in keep or strong & b_strong or len(words & b_words) >= 2:
                kept.setdefault(subject, []).append(b)
    if not kept and scored:
        _, subject, b = max(scored, key=lambda x: x[0])
        kept[subject] = [b]
    return kept


def block_texts(documents: list[Document]) -> dict[str, str]:
    return {b.id: b.text for d in documents for b in d.blocks}


def statement_blocks(
    statement: dict[str, Any],
    results: list[dict[str, Any]],
    record: Record,
    facts: dict[str, Fact],
    texts: dict[str, str] | None = None,
) -> dict[str, list[str]]:
    """Source lines grouped by the items a statement is about: passages and facts it cites
    directly, then the facts of the items it cites (or names from cited rows) whose values it
    states."""
    text = statement["text"]
    events = {e.id for e in record.events}
    groups: dict[str, list[str]] = {}
    for c in statement["cites"]:
        if ":L" in c and c.split(":", 1)[0] in {d["key"] for d in record.documents}:
            groups.setdefault("passage", []).append(c)
        elif c in facts:
            f = facts[c]
            blocks = [
                e.block for e in f.evidence if e.stance in {"supports", "contradicts", "superseded"}
            ]
            groups.setdefault(f.subject, [])
            groups[f.subject] += [b for b in blocks if b not in groups[f.subject]][:3]
        elif c in events:
            groups.setdefault(c, _event_blocks(c, record, text))
    rows = {row["id"]: row for r in results for row in r["rows"]}
    members = [m for c in statement["cites"] if c in rows for m in rows[c].get("members", [])]
    named = [m for m in members if m.lower() in text.lower()]
    direct = set(groups)
    for m in named or members:
        groups.setdefault(m, _event_blocks(m, record, text))
    # the statement's own citations stay; lines reached only through a cited row's members are
    # kept when they share something with the statement
    return prune_blocks(text, groups, texts, direct | set(named)) if texts is not None else groups


def statement_links(
    statement: dict[str, Any],
    results: list[dict[str, Any]],
    record: Record,
    facts: dict[str, Fact],
    documents: dict[str, Document],
) -> str:
    """Links grouped by the items a statement is about."""
    texts = {b.id: b.text for d in documents.values() for b in d.blocks}
    groups = statement_blocks(statement, results, record, facts, texts)
    parts = []
    for subject, blocks in groups.items():
        if not blocks:
            continue
        label = subject if not subject.startswith(("FIN:", "O-")) else "finding"
        parts.append(f"{label}: " + ", ".join(source_link(b, documents) for b in blocks))
    return "; ".join(parts[:20])


def answers_markdown(
    answers: list[dict[str, Any]], record: Record, documents_list: list[Document]
) -> str:
    documents = {d.key: d for d in documents_list}
    facts = {f.id: f for f in record.facts}
    out = [
        "# Answers",
        "",
        "Every number was computed by code from the record; every citation resolves to source lines.",
        "",
    ]
    for a in answers:
        out += [f"## {a['id']}. {a['question']}", ""]
        if a["status"] == "withheld":
            out += (
                ["**Withheld** — the answer failed its checks:", ""]
                + [f"- {r}" for r in a.get("reasons", [])]
                + [""]
            )
        elif a["status"] == "partial" and a.get("reasons"):
            out += (
                ["**Partial** — every statement passed its checks; the reviewer found gaps:", ""]
                + [f"- {r}" for r in a["reasons"]]
                + [""]
            )
        answer = a.get("answer") or {}
        for s in answer.get("statements", []):
            links = statement_links(s, a.get("results", []), record, facts, documents)
            tag = {
                "conflict": " *(conflict)*",
                "missing": " *(not documented)*",
                "inference": " *(inference)*",
            }.get(s["kind"], "")
            out.append(f"- {s['text']}{tag}" + (f" — {links}" if links else ""))
        out.append("")
        if a.get("results"):
            out += ["<details><summary>Calculations</summary>", ""]
            for r in a["results"]:
                out += result_table(r)
            out += ["</details>", ""]
        subjects = {
            m for r in a.get("results", []) for row in r["rows"] for m in row.get("members", [])
        }
        related = [
            o
            for o in record.open_items
            if o.subject in subjects and o.kind in {"conflict", "missing", "candidate_link"}
        ]
        if related:
            out += ["Open items:", ""] + [f"- {o.text}" for o in related] + [""]
    return "\n".join(out) + "\n"
