"""② Extract: one extraction call per document and reading (plus a targeted sweep for what the
first call missed), every value grounded in an exact quote.

The extractor records what the document says. It never calculates, merges records, decides
whether something counts, or fills a value from a schedule. Kinds and fields come from the
policy file, so a new kind of observation is a policy change.
"""

from __future__ import annotations

import hashlib
from typing import Any

from record_engine import llm
from record_engine.ingest import Document
from record_engine.policy import Policy

PROMPT_VERSION = "extract-3"

RULES = """You record what ONE clinical document says, as observations. You do not decide what is
true, what counts, or how records relate beyond what this document itself states.

Every field is {name, value, quote, block}:
- quote: the shortest exact span of the block that states the value, copied character for
  character (same dashes, spacing and capitalisation). For a table row, quote from the row; the
  column header gives the meaning.
- block: the label of the block the quote comes from, exactly as shown (for example "L7" or
  "L1-6").
- value: normalised: dates as YYYY-MM-DD (use the document's year when a row omits it), times as
  HH:MM 24-hour, minutes and numbers as plain numbers, bool as yes/no, list as comma-separated
  items with each item written out in full (for "individual, group, or family psychotherapy"
  write "individual psychotherapy, group psychotherapy, family psychotherapy").
- Omit a field the document does not state. Never guess.

Never:
- calculate anything (no subtraction of times, no totals, no durations the text does not state);
- merge or deduplicate records, or decide whether a contact counts toward anything;
- fill a patient's arrival, departure or contact time from a schedule, a break boundary, or
  another document; a booked slot goes in scheduled_start/scheduled_end only;
- turn a template, a draft, a charge or an authorisation into evidence that care happened.

Provenance of each observation:
- evidence_kind: actual (documents what happened), planned (schedule/booking), billed (charge),
  authorized, templated (system/template text), reported (a copy or summary of another source's
  report, e.g. an imported result).
- attestation: signed, unsigned, draft, auto (system generated) or unknown, for the part of the
  document the observation comes from.
- recorded: record-time stamps for that part (role signed/entered/received/imported/exported/
  prepared/posted, value YYYY-MM-DD or YYYY-MM-DDTHH:MM, quote, block). These are never event
  dates.
- relation: only when the document itself says so. corrects = it corrects another record (list
  the fields it changes, using this schema's field names, e.g. contact "end"); copy_of = it is a
  copy, retransmission or reprint of another record; addendum = it adds to another record.
  target_desc says which record; quote/block show where the document says so.

Observations:
- one doc_meta per document; its title is the document's own heading, never the file name;
- one contact per visit, appointment, phone call, message or outreach attempt the document
  records (including cancelled, no-show and patient-absent ones); a call about a missed visit is
  its own contact, not part of the visit; start/end are the patient's actual presence or contact
  times only; status_reason is the reason the document gives, attached to the contact it explains;
- one charge per billing entry (charge row, claim, payment or reversal), never a contact;
- one interval per further timed segment (break, lost connection, split segment, time with or
  without the patient); a segment's patient_present says whether the patient was there;
- one measurement per instrument administration (and per item score stated);
- one medication per medication decision or mention;
- one plan_goal per measurable threshold (two thresholds are two observations), with basis saying
  whether it is a treatment goal, a payer authorization, a payer limit or a program rule;
- findings for each clinically meaningful statement (symptoms, function, safety, interventions,
  response, plans, social context). Keep each short and faithful; include who reported it.
Cover every date, time, duration, identifier and score in the document with some observation's
quote unless it is a page artefact."""


def kinds_text(policy: Policy) -> str:
    lines = []
    for kind, spec in policy.kinds.items():
        lines.append(f"\n{kind}: {spec['description']}")
        for f in spec["fields"]:
            extra = f" (one of: {', '.join(f['values'])})" if f.get("values") else ""
            lines.append(f"  - {f['name']} [{f['type']}]{extra}: {f['about']}")
    return "\n".join(lines)


def schema(policy: Policy) -> dict[str, Any]:
    grounded = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "value": {"type": "string"},
            "quote": {"type": "string"},
            "block": {"type": "string"},
        },
        "required": ["name", "value", "quote", "block"],
    }
    prov = policy.data["provenance"]
    observation = {
        "type": "object",
        "properties": {
            "kind": {"type": "string", "enum": list(policy.kinds)},
            "fields": {"type": "array", "items": grounded},
            "evidence_kind": {"type": "string", "enum": prov["evidence_kinds"]},
            "attestation": {"type": "string", "enum": prov["attestations"]},
            "recorded": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string", "enum": prov["recorded_roles"]},
                        "value": {"type": "string"},
                        "quote": {"type": "string"},
                        "block": {"type": "string"},
                    },
                    "required": ["role", "value", "quote", "block"],
                },
            },
            "relation": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": prov["relations"]},
                    "target_desc": {"type": "string"},
                    "fields": {"type": "array", "items": {"type": "string"}},
                    "quote": {"type": "string"},
                    "block": {"type": "string"},
                },
                "required": ["type"],
            },
        },
        "required": ["kind", "fields", "evidence_kind", "attestation"],
    }
    return {
        "type": "object",
        "properties": {
            "observations": {"type": "array", "items": observation},
            "dismissed": {
                "type": "array",
                "description": "Only in a targeted re-extraction: listed mentions that carry no fact.",
                "items": {
                    "type": "object",
                    "properties": {
                        "mention": {"type": "string"},
                        "block": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                    "required": ["mention", "block", "reason"],
                },
            },
        },
        "required": ["observations"],
    }


def system_prompt(policy: Policy) -> str:
    return RULES + "\n\nKinds and fields:" + kinds_text(policy)


def local_label(block_id: str) -> str:
    return block_id.split(":", 1)[1]


def document_text(document: Document) -> str:
    return "\n".join(f"[{local_label(b.id)}]\n{b.text}" for b in document.blocks)


def extract(document: Document, policy: Policy) -> dict[str, Any]:
    user = (
        f"Document: {document.filename}\n\nBlocks:\n{document_text(document)}\n\n"
        "Return every observation for this document."
    )
    return llm.call(
        f"extract:{document.key}", system_prompt(policy), user, schema(policy), llm.WRITER
    )


def re_extract(
    document: Document, policy: Policy, uncovered: list[tuple[str, str, str]]
) -> dict[str, Any]:
    """Targeted pass: blocks with mentions no observation covered."""
    listing = "\n".join(f"- [{local_label(b)}] {kind}: {text!r}" for b, kind, text in uncovered)
    blocks = {b for b, _, _ in uncovered}
    shown = "\n".join(f"[{local_label(b.id)}]\n{b.text}" for b in document.blocks if b.id in blocks)
    user = (
        f"Document: {document.filename}\n\nFull document for context:\n"
        f"{document_text(document)}\n\nThese mentions are not yet covered by any observation:\n"
        f"{listing}\n\nBlocks to re-read:\n{shown}\n\nReturn observations that cover them (the "
        "same rules apply), and list under dismissed any mention that states no fact (with a "
        "reason). Do not repeat observations that other mentions already cover."
    )
    return llm.call(
        f"sweep:{document.key}", system_prompt(policy), user, schema(policy), llm.WRITER
    )


def observation_id(document: Document, index: int, source: str) -> str:
    # the document key is part of the ID: two byte-identical files are still two documents
    digest = hashlib.sha256(
        f"{document.key}:{document.sha256}:{source}:{index}".encode()
    ).hexdigest()[:8]
    return f"O-{digest}"


def to_raw(document: Document, output: dict[str, Any], source: str) -> list[dict[str, Any]]:
    """Attach IDs and full block IDs; validation happens separately."""
    prefix = f"{document.key}:"
    raw = []
    for index, item in enumerate(llm.as_list(output.get("observations"), ("kind", "fields"))):
        fields = [
            {**f, "block": prefix + str(f.get("block", "")).strip("[] ")}
            for f in llm.as_list(item.get("fields"), ("name",))
        ]
        recorded = [
            {**r, "block": prefix + str(r.get("block", "")).strip("[] ")}
            for r in llm.as_list(item.get("recorded"), ("role", "value"))
        ]
        relation_items = llm.as_list(item.get("relation"), ("type",))
        relation = dict(relation_items[0]) if relation_items else {"type": "none"}
        if relation.get("block"):
            relation["block"] = prefix + str(relation["block"]).strip("[] ")
        raw.append(
            {
                "id": observation_id(document, index, source),
                "doc": document.key,
                "kind": item.get("kind"),
                "fields": fields,
                "evidence_kind": item.get("evidence_kind", "actual"),
                "attestation": item.get("attestation", "unknown"),
                "recorded": recorded,
                "relation": relation,
                "source": source,
            }
        )
    return raw
