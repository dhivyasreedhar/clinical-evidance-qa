"""⑤ Reconcile (code + policy): per event and field → one fact with status, rule and evidence.

For each event and field:
  1. admissible — drop claims whose evidence kind cannot answer the field (policy.admissible);
  2. supersede — a correction replaces earlier claims for the fields it names (the latest
     correction by record time wins); a copy stands or falls with its original;
  3. rank     — attestation (policy.attestation_rank: signed > unknown > unsigned > draft/auto),
     then contemporaneous > later;
  4. decide   — one value in the top tier: documented (one independent source), corroborated
     (several independent sources agree) or established (a rule removed a disagreement); several
     values in the top tier: conflicting, every value kept as a scenario.
Copies never count as independent sources. Record times (signature, receipt, import) never
create an event. Creditable minutes are computed per scenario: patient presence minus breaks and
gaps, by interval algebra. Open items are computed here too; no model is used.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import date, timedelta
from typing import Any

from record_engine import VERSION
from record_engine.ingest import Document
from record_engine.link import detect_copies, id_key, link, norm
from record_engine.model import Event, Evidence, Fact, Observation, OpenItem, Record
from record_engine.policy import Policy
from record_engine.values import clock

# observation field -> reconciled field it speaks to (for corrections that name fields)
FIELD_ALIASES = {
    "start": "presence_start",
    "arrival": "presence_start",
    "end": "presence_end",
    "departure": "presence_end",
    "status_claim": "status",
    "patient_present": "attendance",
    "stated_minutes": "stated_minutes",
    "service": "service",
    "date": "date",
    "score": "score",
}


# status claims under which a contact's times are not the patient's presence (missed, cancelled,
# held without the patient, or only booked)
NOT_PRESENT_CLAIMS = {
    "no_show",
    "cancelled_by_patient",
    "cancelled_by_clinic",
    "cancelled_unspecified",
    "not_present",
    "scheduled",
}


class Claim:
    def __init__(
        self,
        field: str,
        value: Any,
        obs: Observation,
        blocks: list[tuple[str, str]],
        copy: bool,
        recorded: str | None,
    ):
        self.field, self.value, self.obs, self.copy, self.recorded = (
            field,
            value,
            obs,
            copy,
            recorded,
        )
        self.blocks = blocks  # (block, quote)


def fact_id(subject: str, field: str) -> str:
    return "F-" + hashlib.sha256(f"{subject}|{field}".encode()).hexdigest()[:8]


def record_time(
    o: Observation, copy: bool, doc_times: dict[str, str], authoring: set[str] | None = None
) -> str | None:
    """When the account was recorded. A copy carries its original's time (earliest signature).
    Authoring times (signature, entry) are used when the account has them: an extract prepared
    or exported later does not make the row it reproduces a later account."""
    times = [r.value for r in o.recorded]
    authored = [r.value for r in o.recorded if authoring and r.role in authoring]
    if authored and not copy:
        return max(authored)
    if copy:
        signed = [r.value for r in o.recorded if r.role == "signed"]
        return min(signed or times) if (signed or times) else doc_times.get(o.doc)
    return max(times) if times else doc_times.get(o.doc)


def contemporaneous(recorded: str | None, event_day: str | None, days: int) -> bool | None:
    """True = recorded at the time of the event, False = later, None = unknown."""
    if not recorded or not event_day:
        return None
    try:
        delta = date.fromisoformat(recorded[:10]) - date.fromisoformat(event_day[:10])
    except ValueError:
        return None
    return delta <= timedelta(days=days)


def corrects(o: Observation) -> bool:
    """A correction, or an addendum that names the fields it changes (a late entry correcting the
    arrival time is a correction of that field, whichever word the record uses)."""
    return o.relation.type == "corrects" or (
        o.relation.type == "addendum" and bool(o.relation.fields)
    )


def corrected_fields(o: Observation) -> set[str]:
    fields = set()
    for name in o.relation.fields:
        key = norm(name).replace(" ", "_")
        fields.add(FIELD_ALIASES.get(key, key))
    if fields & {"status", "attendance"}:
        fields |= {"status", "attendance"}  # attendance is derived from status
    return fields


def decide(
    subject: str,
    field: str,
    claims: list[Claim],
    policy: Policy,
    event_day: str | None,
) -> Fact | None:
    admissible = [c for c in claims if policy.admits(field, c.obs.evidence_kind)]
    rejected = [c for c in claims if c not in admissible]
    if not admissible:
        return None
    evidence: list[Evidence] = []

    def ev(c: Claim, stance: str) -> list[Evidence]:
        return [
            Evidence(observation=c.obs.id, block=b, quote=q, stance=stance, value=c.value)
            for b, q in c.blocks
        ]

    # 2. supersede: corrections for this field, latest record time wins
    corrections = sorted(
        (c for c in admissible if corrects(c.obs) and field in corrected_fields(c.obs)),
        key=lambda c: c.recorded or "",
    )
    superseded: list[Claim] = []
    rule = ""
    reason = ""
    live = admissible
    if corrections:
        winner = corrections[-1]
        cutoff = winner.recorded or "9999"
        superseded = [
            c
            for c in admissible
            if c is not winner and (c.recorded or "") <= cutoff and c.value != winner.value
        ]
        live = [c for c in admissible if c not in superseded]
        if superseded:
            rule = "signed_correction_supersedes_original"
            reason = (
                f"A correction recorded {winner.recorded or 'later'} replaces the earlier value"
                + (
                    " (copies of the original fall with it)"
                    if any(c.copy for c in superseded)
                    else ""
                )
            )

    # a generic value is refined by a categorised one, not contradicted by it
    refined: list[Claim] = []
    if field in policy.refine:
        present_values = {c.value for c in live}
        refined = [c for c in live if policy.refined_by(field, c.value, present_values)]
        live = [c for c in live if c not in refined]
        if refined and not rule:
            rule = "specific_refines_generic"
            reason = (
                "A generic description ("
                + ", ".join(sorted({str(c.value) for c in refined}))
                + ") is refined by a specific one."
            )

    # 3. rank the remaining claims. Timing is three-valued (at the time / later / unknown): it
    # ranks claims only when every competing claim's timing is known, so a record time the
    # extractor missed can never settle a conflict.
    timing = {
        id(c): contemporaneous(c.recorded, event_day, policy.contemporaneous_days) for c in live
    }
    use_timing = all(t is not None for t in timing.values())

    def rank(c: Claim) -> tuple[int, int]:
        return (
            policy.rank.get(c.obs.attestation, policy.rank.get("unknown", 0)),
            1 if use_timing and timing[id(c)] else 0,
        )

    top = max(rank(c) for c in live)
    top_claims = [c for c in live if rank(c) == top]
    outranked = [c for c in live if rank(c) != top]
    values: list[Any] = []
    for c in top_claims:
        if c.value not in values:
            values.append(c.value)
    outranked_differ = [c for c in outranked if c.value not in values]
    # independent documents that state the winning value (outranked agreeing accounts count)
    independent_docs = {c.obs.doc for c in live if not c.copy and c.value in values}

    for c in top_claims:
        evidence += ev(c, "copy" if c.copy else "supports")
    for c in outranked:
        evidence += ev(
            c,
            "copy"
            if c.copy and c.value in values
            else ("supports" if c.value in values else "contradicts"),
        )
    for c in superseded:
        evidence += ev(c, "superseded")
    for c in refined:
        evidence += ev(c, "supports")

    if len(values) > 1:
        status, rule, reason = (
            "conflicting",
            "no_rule_applies",
            "Sources of equal standing disagree; every value is kept as a scenario.",
        )
    elif rule == "specific_refines_generic":
        status = (
            "corroborated"
            if len(independent_docs | {c.obs.doc for c in refined if not c.copy}) >= 2
            else "documented"
        )
    elif rule:
        status = "established"
    elif outranked_differ:
        status, rule = "established", "precedence"
        reason = (
            "Outranked accounts ("
            + ", ".join(sorted({f"{c.obs.attestation}" for c in outranked_differ}))
            + ") disagree; the higher-ranked account stands."
        )
    elif len(independent_docs) >= 2:
        status, rule, reason = (
            "corroborated",
            "independent_sources_agree",
            f"{len(independent_docs)} independent documents agree.",
        )
    else:
        status, rule = "documented", "single_source"
        reason = (
            "One independent source"
            + (" (copies add no independent support)" if any(c.copy for c in top_claims) else "")
            + "."
        )
    if rejected:
        reason += (
            " Inadmissible for this field: "
            + ", ".join(sorted({c.obs.evidence_kind for c in rejected}))
            + "."
        )
    recorded = max((c.recorded for c in top_claims if c.recorded), default=None)
    return Fact(
        id=fact_id(subject, field),
        subject=subject,
        field=field,
        value=values[0] if len(values) == 1 else None,
        scenarios=values if len(values) > 1 else [],
        status=status,
        rule=rule,
        reason=reason.strip(),
        valid_time=event_day,
        recorded_time=recorded,
        evidence=evidence,
    )


# --- interval algebra ------------------------------------------------------------------------


def creditable_minutes(start: str, end: str, holes: list[tuple[str, str]]) -> float | None:
    s, e = clock(start), clock(end)
    if e <= s:
        return None
    clipped = sorted((max(s, clock(a)), min(e, clock(b))) for a, b in holes)
    clipped = [(a, b) for a, b in clipped if b > a]
    removed, cursor = 0, s
    for a, b in clipped:
        a = max(a, cursor)
        if b > a:
            removed += b - a
            cursor = b
    return float(e - s - removed)


def account_segments(
    obs: list[Observation],
) -> tuple[list[tuple[str, str, Observation]], list[tuple[str, str, Observation]]]:
    """Patient-present segments and non-service holes (breaks, gaps) in one document's account.

    An interval that explicitly records the patient present is more specific than the contact's
    own start and end (which may be the whole session): when a document has such intervals, they
    are the presence. Intervals that explicitly record the patient absent are gaps."""
    explicit = [
        (str(o.get("start")), str(o.get("end")), o)
        for o in obs
        if o.kind == "interval"
        and o.get("start")
        and o.get("end")
        and o.get("patient_present") == "yes"
        and (o.get("role") or "presence") in {"presence", "service"}
    ]
    present: list[tuple[str, str, Observation]] = []
    holes: list[tuple[str, str, Observation]] = []
    for o in obs:
        s, e = o.get("start"), o.get("end")
        if not (s and e):
            continue
        if o.kind == "contact":
            # a contact's own times are presence only when the patient was there and no interval
            # records the presence more precisely; a missed or cancelled contact has none
            if (
                o.get("patient_present") != "no"
                and o.get("status_claim") not in NOT_PRESENT_CLAIMS
                and not explicit
            ):
                present.append((s, e, o))
            continue
        role = o.get("role") or "other"
        if role in {"presence", "service"} and o.get("patient_present") != "no":
            present.append((s, e, o))
        elif role in {"break", "gap"} or (
            o.kind == "interval" and o.get("patient_present") == "no"
        ):
            holes.append((s, e, o))
    return present, holes


# --- the record ------------------------------------------------------------------------------


IDENTITY_FIELDS = ["patient_name", "patient_dob", "patient_mrn"]
GOAL_BASES = {"treatment_goal", "program_rule"}


def patient_scope(
    observations: list[Observation], policy: Policy
) -> tuple[list[Observation], dict[str, str], dict[str, str | None]]:
    """Keep only documents about the record's patient.

    Identity is the record number and date of birth each document's header states (never the
    name alone). The patient is the one configured in the policy ([patient] mrn / dob), else the
    record number most documents state. A document whose stated MRN or DOB differs is set aside
    with an open item; a document stating neither stays (it cannot be shown to be someone else).
    Returns (observations in scope, document -> reason set aside, the patient identity used)."""
    from collections import Counter

    stated: dict[str, dict[str, str]] = defaultdict(dict)
    shown: dict[str, str] = {}  # normalized record number -> as written
    for o in observations:
        if o.kind != "doc_meta":
            continue
        for name, key in (("patient_mrn", "mrn"), ("patient_dob", "dob")):
            value = o.get(name)
            if value and key not in stated[o.doc]:
                stated[o.doc][key] = id_key(value) if key == "mrn" else str(value)[:10]
                if key == "mrn":
                    shown.setdefault(id_key(value), str(value))
    configured = policy.data.get("patient", {})
    mrn = id_key(configured.get("mrn")) if configured.get("mrn") else None
    dob = str(configured["dob"])[:10] if configured.get("dob") else None
    if not mrn:
        counts = Counter(v["mrn"] for v in stated.values() if v.get("mrn"))
        ranked = counts.most_common(2)
        if ranked and (len(ranked) == 1 or ranked[0][1] > ranked[1][1]):
            mrn = ranked[0][0]
    if not dob and mrn:
        dobs = Counter(v["dob"] for v in stated.values() if v.get("mrn") == mrn and v.get("dob"))
        dob = dobs.most_common(1)[0][0] if dobs else None
    aside: dict[str, str] = {}
    for doc, ident in stated.items():
        reasons = []
        if mrn and ident.get("mrn") and ident["mrn"] != mrn:
            reasons.append(
                f"MRN {shown.get(ident['mrn'], ident['mrn'])} is not the record's patient "
                f"({shown.get(mrn, configured.get('mrn') or mrn)})"
            )
        if dob and ident.get("dob") and ident["dob"] != dob:
            reasons.append(f"date of birth {ident['dob']} is not the record's patient ({dob})")
        if reasons:
            aside[doc] = "; ".join(reasons)
    kept = [o for o in observations if o.doc not in aside]
    return kept, aside, {"mrn": mrn, "dob": dob}


def inherit_document_relations(observations: list[Observation]) -> list[Observation]:
    """A relation the document states about itself (on its doc_meta: "this corrects...", "this is
    a copy of...") applies to the document's other observations that state none, so a correction
    works whichever observation the extractor attached it to."""
    stated = {
        o.doc: o.relation
        for o in observations
        if o.kind == "doc_meta" and o.relation.type not in {"none", ""}
    }
    return [
        o.model_copy(update={"relation": stated[o.doc]})
        if o.doc in stated and o.kind != "doc_meta" and o.relation.type in {"none", ""}
        else o
        for o in observations
    ]


def build_record(
    documents: list[Document],
    observations: list[Observation],
    policy: Policy,
    extraction_issues: list[OpenItem] | None = None,
) -> Record:
    observations, set_aside, _patient = patient_scope(observations, policy)
    observations = inherit_document_relations(observations)
    obs_by_id = {o.id: o for o in observations}
    copies, copy_obs = detect_copies(
        [d for d in documents if d.key not in set_aside], observations, policy
    )
    events, event_of, open_items = link(observations, policy)
    # narrative findings of a document that is a copy of another are the original's findings
    # again: they are not separate facts
    events = [
        e
        for e in events
        if not (e.kind == "finding" and all(obs_by_id[i].doc in copies for i in e.observations))
    ]
    authoring = set(policy.data["precedence"].get("authoring_roles", []))
    doc_times: dict[str, str] = {}
    for o in observations:
        stamps = [r for r in o.recorded if r.role in authoring] or o.recorded
        for r in stamps:
            doc_times[o.doc] = max(doc_times.get(o.doc, ""), r.value)
    facts: list[Fact] = []

    def claim(field: str, value: Any, o: Observation, names: list[str]) -> Claim:
        grounded = [o.field(n) for n in names]
        blocks = [(g.block, g.quote) for g in grounded if g]
        copy = o.id in copy_obs
        return Claim(
            field,
            value,
            o,
            blocks,
            copy,
            record_time(o, copy, doc_times, authoring),
        )

    doc_contact_dates_all: dict[str, set[str]] = defaultdict(set)
    for o in observations:
        if o.kind in {"contact", "interval"} and o.get("date"):
            doc_contact_dates_all[o.doc].add(str(o.get("date")))
    titles = {
        o.doc: str(o.get("title")) for o in observations if o.kind == "doc_meta" and o.get("title")
    }
    # eligible services come from the care goals
    # Only care goals define what counts; an authorization or payer limit is not a goal the care is
    # judged against (the same rule goal_met() applies).
    eligible: set[str] = set()
    for o in observations:
        if (
            o.kind == "plan_goal"
            and o.get("eligible_services")
            and (o.get("basis") or "treatment_goal") in GOAL_BASES
        ):
            eligible |= {
                policy.service(s.strip()) or ""
                for s in (o.get("eligible_services") or "").split(",")
                if s.strip()
            }
    eligible.discard("")

    for event in events:
        members = [obs_by_id[i] for i in event.observations]
        if event.kind == "encounter":
            facts += encounter_facts(
                event, members, policy, claim, eligible, open_items, titles, set(copies)
            )
            probable = next(
                (
                    o.facts[0]
                    for o in open_items
                    if o.kind == "candidate_link" and o.subject == event.id and o.facts
                ),
                None,
            )
            if probable:
                for f in facts:
                    if (
                        f.subject == event.id
                        and f.field == "disposition"
                        and f.value == "no_actual_record"
                    ):
                        f.reason = (
                            f"a reference to a visit, probably {probable} (same date and service); "
                            f"that visit is documented and counted there, not here"
                        )
        elif event.kind == "measurement":
            facts += simple_facts(
                event,
                members,
                ["score", "interpretation", "completed_on", "instrument", "item", "form_id"],
                policy,
                claim,
            )
        elif event.kind == "goal":
            facts += simple_facts(
                event,
                members,
                [
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
                ],
                policy,
                claim,
            )
        elif event.kind == "charge":
            facts += simple_facts(
                event,
                members,
                [
                    "charge_id",
                    "encounter_id",
                    "date",
                    "service",
                    "code",
                    "quantity",
                    "status",
                    "amount",
                ],
                policy,
                claim,
            )
        elif event.kind == "medication":
            facts += simple_facts(
                event, members, ["name", "dose", "schedule", "change", "date"], policy, claim
            )
        elif event.kind == "finding":
            facts += simple_facts(
                event, members, ["text", "type", "reporter", "date", "encounter_id"], policy, claim
            )
        elif event.kind == "document":
            # what each document's header states about itself and the patient; its title and
            # issuer are wording, listed as written rather than decided between
            headers = [o for o in members if o.kind == "doc_meta"]
            for name, about in (
                ("title", "The document's heading as written."),
                ("issuer", "Who the document says issued it, as written."),
            ):
                listed = listed_fact(
                    event.id,
                    name,
                    [(str(o.get(name)), o, name) for o in headers if o.get(name)],
                    None,
                    about,
                )
                if listed:
                    facts.append(listed)
            facts += simple_facts(
                event,
                headers,
                [
                    "document_id",
                    "patient_name",
                    "patient_dob",
                    "patient_mrn",
                    "episode_start",
                    "episode_end",
                ],
                policy,
                claim,
            )

    # a contact without its own stated date (a call logged under a dated header) takes the date
    # its document gives all its dated contacts, when there is exactly one
    for event in events:
        if event.kind != "encounter" or any(
            f.subject == event.id and f.field == "date" for f in facts
        ):
            continue
        docs = {obs_by_id[i].doc for i in event.observations}
        doc_days = {d for doc in docs for d in doc_contact_dates_all.get(doc, set())}
        if len(doc_days) == 1:
            day = next(iter(doc_days))
            facts.append(
                Fact(
                    id=fact_id(event.id, "date"),
                    subject=event.id,
                    field="date",
                    value=day,
                    status="documented",
                    rule="date_from_document",
                    reason="The contact states no date; its document dates all its contacts to this day.",
                    valid_time=day,
                )
            )

    # a finding without its own stated date takes the date of the encounter it was recorded in
    # (by encounter ID, else its document's only dated contact); the rule says so
    dated = {f.subject: f for f in facts if f.field == "date"}
    doc_contact_dates: dict[str, set[str]] = defaultdict(set)
    for o in observations:
        if o.kind == "contact" and o.get("date"):
            doc_contact_dates[o.doc].add(str(o.get("date")))
    for event in events:
        if event.kind != "finding" or event.id in dated:
            continue
        o = obs_by_id[event.observations[0]]
        source = event_of.get(
            next(
                (
                    x.id
                    for x in observations
                    if x.kind in {"contact", "interval"}
                    and id_key(x.get("encounter_id")) == id_key(o.get("encounter_id"))
                    and o.get("encounter_id")
                ),
                "",
            ),
            "",
        )
        if source and source in dated:
            day, why = dated[source].value, f"date of encounter {source}"
        elif len(doc_contact_dates[o.doc]) == 1:
            day, why = next(iter(doc_contact_dates[o.doc])), "date of the document's only encounter"
        else:
            continue
        facts.append(
            Fact(
                id=fact_id(event.id, "date"),
                subject=event.id,
                field="date",
                value=day,
                status="documented",
                rule="inherited_from_encounter",
                reason=f"Finding carries no stated date; it takes the {why}.",
                valid_time=day,
            )
        )

    # the patient: identity stated in the headers of the documents in scope
    identity_obs = [
        o for o in observations if o.kind == "doc_meta" and any(o.get(n) for n in IDENTITY_FIELDS)
    ]
    if identity_obs:
        patient_event = Event(
            id="patient", kind="patient", observations=[o.id for o in identity_obs]
        )
        events.append(patient_event)
        facts += simple_facts(patient_event, identity_obs, IDENTITY_FIELDS, policy, claim)
    for doc, reason in sorted(set_aside.items()):
        open_items.append(
            OpenItem(
                kind="other_patient",
                subject=doc,
                text=f"{doc} was set aside: {reason}. None of its content is in this record.",
            )
        )

    for f in facts:
        if f.status == "conflicting":
            open_items.append(
                OpenItem(
                    kind="conflict",
                    subject=f.subject,
                    text=f"{f.subject} {f.field}: "
                    + " or ".join(str(v) for v in f.scenarios)
                    + " — "
                    + f.reason,
                    blocks=sorted({e.block for e in f.evidence}),
                    facts=[f.id],
                )
            )
    open_items += extraction_issues or []

    doc_rows = []
    for d in documents:
        meta = next((o for o in observations if o.doc == d.key and o.kind == "doc_meta"), None)
        doc_rows.append(
            {
                "key": d.key,
                "filename": d.filename,
                "sha256": d.sha256,
                "title": meta.get("title") if meta else None,
                "issuer": meta.get("issuer") if meta else None,
                "copy_of": copies.get(d.key),
                "set_aside": set_aside.get(d.key),
                "copy_observations": sum(
                    1 for o in observations if o.doc == d.key and o.id in copy_obs
                ),
                "observations": sum(1 for o in observations if o.doc == d.key),
            }
        )
    return Record(
        version=VERSION,
        policy=policy.version,
        documents=doc_rows,
        events=events,
        facts=facts,
        open_items=open_items,
        copies=copies,
    )


def simple_facts(
    event: Event, members: list[Observation], fields: list[str], policy: Policy, claim: Any
) -> list[Fact]:
    facts = []
    day = next(
        (
            o.get("completed_on") or o.get("date") or o.get("effective_start")
            for o in members
            if o.get("completed_on") or o.get("date") or o.get("effective_start")
        ),
        None,
    )
    for field in fields:
        claims = []
        for o in members:
            text = o.get(field)
            if text is None:
                continue
            value: Any = float(text) if field == "score" else text
            claims.append(claim(field, value, o, [field]))
        if claims:
            fact = decide(event.id, field, claims, policy, day)
            if fact:
                facts.append(fact)
    return facts


def listed_fact(
    subject: str,
    field: str,
    items: list[tuple[str, Observation, str]],
    day: str | None,
    reason: str,
) -> Fact | None:
    """A fact whose value is the list of distinct values the records state (participants,
    reasons, records): nothing is decided between them, every value is kept with its source."""
    values: list[str] = []
    evidence: list[Evidence] = []
    for value, o, name in items:
        if value not in values:
            values.append(value)
        g = o.field(name)
        if g:
            evidence.append(Evidence(observation=o.id, block=g.block, quote=g.quote, value=value))
    if not values:
        return None
    docs = {o.doc for _, o, _ in items}
    return Fact(
        id=fact_id(subject, field),
        subject=subject,
        field=field,
        value=values,
        status="corroborated" if len(docs) > 1 and len(values) == 1 else "documented",
        rule="as_documented",
        reason=reason,
        valid_time=day,
        evidence=evidence,
    )


def encounter_facts(
    event: Event,
    members: list[Observation],
    policy: Policy,
    claim: Any,
    eligible: set[str],
    open_items: list[OpenItem],
    titles: dict[str, str] | None = None,
    copies: set[str] | None = None,
) -> list[Fact]:
    facts: list[Fact] = []
    dates = [o.get("date") for o in members if o.get("date")]
    day = max(set(dates), key=dates.count) if dates else None

    def add(field: str, claims: list[Claim]) -> Fact | None:
        if not claims:
            return None
        fact = decide(event.id, field, claims, policy, day)
        if fact:
            facts.append(fact)
        return fact

    add("date", [claim("date", o.get("date"), o, ["date"]) for o in members if o.get("date")])
    add(
        "service",
        [
            claim("service", policy.service(o.get("service")), o, ["service"])
            for o in members
            if o.kind == "contact" and o.get("service")
        ],
    )
    # what the records say about the contact beyond the decided fields: who took part, how,
    # when it was booked, and any reason given for its status (all kept, with their sources)
    actual = [o for o in members if o.evidence_kind not in {"billed", "authorized"}]
    for field, name, reason in (
        ("participants", "participants", "People the records name for this contact."),
        ("mode", "mode", "How the contact happened, as written."),
        ("status_reason", "status_reason", "Reasons the records give for the attendance status."),
    ):
        items = [(str(o.get(name)), o, name) for o in actual if o.get(name)]
        fact = listed_fact(event.id, field, items, day, reason)
        if fact:
            facts.append(fact)
    booked = [
        claim(
            "scheduled",
            f"{o.get('scheduled_start')}–{o.get('scheduled_end')}",
            o,
            ["scheduled_start", "scheduled_end"],
        )
        for o in members
        if o.kind == "contact" and o.get("scheduled_start") and o.get("scheduled_end")
    ]
    add("scheduled", booked)
    titles = titles or {}
    records: list[tuple[str, Observation, str]] = []
    # one entry per document: a document that records the contact first-hand is an actual
    # record, whatever else it carries (an attached export or an addendum inside the same note
    # is part of that record, not another record of the contact)
    per_document: dict[str, list[Observation]] = {}
    for o in members:
        per_document.setdefault(o.doc, []).append(o)
    for doc, observed in per_document.items():
        first_hand = [o for o in observed if o.evidence_kind == "actual"]
        o = (first_hand or observed)[0]
        relations = {x.relation.type for x in observed}
        role = (
            o.evidence_kind
            + (", copy" if doc in (copies or set()) or "copy_of" in relations else "")
            + (", corrects" if "corrects" in relations else "")
            + (", addendum" if o.relation.type == "addendum" else "")
        )
        entry = f"{titles.get(doc, doc)} ({role})"
        g = next(iter(o.fields), None)
        if entry not in [r[0] for r in records] and g:
            records.append((entry, o, g.name))
    fact = listed_fact(
        event.id, "records", records, day, "Documents that record this contact, with their role."
    )
    if fact:
        facts.append(fact)

    # what happened to the appointment, reconciled like any other field (conflicts included);
    # attendance is derived from the same claims through the policy mapping
    status_fact = add(
        "status",
        [
            claim("status", o.get("status_claim"), o, ["status_claim"])
            for o in members
            if o.kind == "contact" and o.get("status_claim") not in {None, "scheduled", "unknown"}
        ],
    )
    attendance = []
    for o in members:
        if o.kind != "contact":
            continue
        if o.get("patient_present") == "no" or o.get("status_claim") in policy.not_attended:
            attendance.append(
                claim("attendance", "not_attended", o, ["patient_present", "status_claim"])
            )
        elif o.get("status_claim") in policy.attended or o.get("patient_present") == "yes":
            attendance.append(
                claim("attendance", "attended", o, ["status_claim", "patient_present"])
            )
    attended = add("attendance", attendance)

    # presence per document account (min start / max end of that document's patient segments);
    # each account keeps its own breaks and gaps, so minutes are never combined across accounts
    by_doc: dict[str, list[Observation]] = defaultdict(list)
    for o in members:
        by_doc[o.doc].append(o)
    starts, ends, stated = [], [], []
    accounts: list[dict[str, Any]] = []
    shared: dict[str, list[Claim]] = {}  # break-only documents: doc -> its break claims
    for doc, obs in by_doc.items():
        present, doc_holes = account_segments(obs)
        own: list[Claim] = [
            claim("breaks", (hs, he), o, ["start", "end"])
            for hs, he, o in doc_holes
            if policy.admits("breaks", o.evidence_kind)
        ]
        if present:
            first = min(present, key=lambda p: clock(p[0]))
            last = max(present, key=lambda p: clock(p[1]))
            # a segment the document records without the patient at the start or end of the
            # session (a partner-only opening, an early exit) moves the patient's own arrival or
            # departure to its edge; creditable minutes are unchanged (holes are subtracted)
            start = (first[0], first[2], "start")
            end = (last[1], last[2], "end")
            absent = [
                (hs, he, o)
                for hs, he, o in doc_holes
                if o.kind == "interval" and o.get("patient_present") == "no"
            ]
            moved = True
            while moved:
                moved = False
                for hs, he, o in absent:
                    if clock(hs) <= clock(start[0]) < clock(he) < clock(end[0]):
                        start, moved = (he, o, "end"), True
                    if clock(start[0]) < clock(hs) < clock(end[0]) <= clock(he):
                        end, moved = (hs, o, "start"), True
            start_claim = claim("presence_start", start[0], start[1], [start[2]])
            end_claim = claim("presence_end", end[0], end[1], [end[2]])
            starts.append(start_claim)
            ends.append(end_claim)
            # holes between one account's own patient segments are gaps in contact
            ordered = sorted(present, key=lambda p: clock(p[0]))
            for (_a, b, oa), (c, _d, ob) in zip(ordered, ordered[1:], strict=False):
                if clock(c) > clock(b):
                    gap = claim("breaks", (b, c), oa, ["end"])
                    gap.blocks += [(g.block, g.quote) for g in [ob.field("start")] if g]
                    own.append(gap)
            accounts.append({"doc": doc, "start": start_claim, "end": end_claim, "holes": own})
        else:
            # start or end stated alone
            for o in obs:
                if o.kind == "contact" and o.get("start") and not o.get("end"):
                    starts.append(claim("presence_start", o.get("start"), o, ["start"]))
                if o.kind == "contact" and o.get("end") and not o.get("start"):
                    ends.append(claim("presence_end", o.get("end"), o, ["end"]))
            if own:
                shared[doc] = own
        # a duration stated for an explicit patient-present segment is the patient's stated time;
        # the contact's own stated duration may be the whole session (same rule as presence)
        segment_stated = [
            o
            for o in obs
            if o.kind == "interval"
            and o.get("patient_present") == "yes"
            and (o.get("role") or "presence") in {"presence", "service"}
            and o.get("stated_minutes")
        ]
        if segment_stated:
            total = claim(
                "stated_minutes",
                sum(float(o.get("stated_minutes") or 0) for o in segment_stated),
                segment_stated[0],
                ["stated_minutes"],
            )
            for o in segment_stated[1:]:
                total.blocks += [(g.block, g.quote) for g in [o.field("stated_minutes")] if g]
            stated.append(total)
        for o in obs if not segment_stated else []:
            if o.kind == "contact" and o.get("stated_minutes"):
                stated.append(
                    claim(
                        "stated_minutes", float(o.get("stated_minutes") or 0), o, ["stated_minutes"]
                    )
                )
    start_fact = add("presence_start", starts)
    end_fact = add("presence_end", ends)
    scheduled_fact = next(
        (f for f in facts if f.subject == event.id and f.field == "scheduled"), None
    )
    # attended part of the booking: the patient's documented presence starts after the booked
    # start or ends before the booked end (code decides this from the times, not the wording)
    if (
        status_fact
        and status_fact.value == "attended"
        and status_fact.status != "conflicting"
        and start_fact
        and end_fact
        and scheduled_fact
        and len(start_fact.values()) == 1
        and len(end_fact.values()) == 1
        and scheduled_fact.status != "conflicting"
    ):
        booked_start, _, booked_end = str(scheduled_fact.value).partition("–")
        arrived, left = str(start_fact.values()[0]), str(end_fact.values()[0])
        if (
            booked_start
            and booked_end
            and (clock(arrived) > clock(booked_start) or clock(left) < clock(booked_end))
        ):
            status_fact.value = "partial"
            status_fact.rule = "presence_within_booking"
            status_fact.reason = (
                f"Present {arrived}–{left} of the booked {booked_start}–{booked_end}: attended "
                "part of it."
            )
            status_fact.evidence += [
                e for f in (start_fact, end_fact, scheduled_fact) for e in f.evidence
            ]
    # A duration a document states alongside its own start and end is the length of that
    # interval. When a correction supersedes the start or end, the duration restating the old
    # interval falls with it (the correction's own duration, if any, stands).
    fallen: list[Claim] = []
    for acc in accounts:
        superseded_times = (start_fact and acc["start"].value not in start_fact.values()) or (
            end_fact and acc["end"].value not in end_fact.values()
        )
        if not superseded_times:
            continue
        old = {
            v
            for v in (
                creditable_minutes(acc["start"].value, acc["end"].value, []),
                creditable_minutes(
                    acc["start"].value, acc["end"].value, [c.value for c in acc["holes"]]
                ),
            )
            if v is not None
        }
        fallen += [c for c in stated if c.obs.doc == acc["doc"] and float(c.value) in old]
    stated = [c for c in stated if c not in fallen]
    stated_fact = add("stated_minutes", stated)
    if stated_fact and fallen:
        stated_fact.reason += (
            " A stated duration that restated superseded times fell with them: "
            + ", ".join(f"{c.value:g} min ({c.obs.doc})" for c in fallen)
            + "."
        )
        stated_fact.evidence += [
            Evidence(observation=c.obs.id, block=b, quote=q, stance="superseded", value=c.value)
            for c in fallen
            for b, q in c.blocks
        ]

    # breaks documented outside any presence account: each document's set of breaks is one
    # account of them; a later correction naming breaks replaces earlier sets; distinct sets
    # that remain are break scenarios
    correcting = [
        d
        for d, cl in shared.items()
        if any(corrects(c.obs) and "breaks" in corrected_fields(c.obs) for c in cl)
    ]
    if correcting:
        latest = max(correcting, key=lambda d: max((c.recorded or "") for c in shared[d]))
        shared = {latest: shared[latest]}
    break_sets: list[tuple[tuple[str, str], ...]] = []
    for cl in shared.values():
        key = tuple(sorted({c.value for c in cl}))
        if key not in break_sets:
            break_sets.append(key)
    if not break_sets:
        break_sets = [()]

    # surviving accounts: both of their values survived reconciliation
    def survives(acc: dict[str, Any]) -> bool:
        return bool(
            start_fact
            and end_fact
            and acc["start"].value in start_fact.values()
            and acc["end"].value in end_fact.values()
        )

    alive = [acc for acc in accounts if survives(acc)]
    minutes: list[float] = []
    used_breaks: dict[tuple[str, str], list[Claim]] = defaultdict(list)
    basis = ""
    if alive:
        for acc in alive:
            own_holes = [c.value for c in acc["holes"]]
            for c in acc["holes"]:
                used_breaks[c.value].append(c)
            options = [tuple(own_holes)] if acc["holes"] else break_sets
            for holes_set in options:
                value = creditable_minutes(acc["start"].value, acc["end"].value, list(holes_set))
                if value is not None and value not in minutes:
                    minutes.append(value)
        basis = "each surviving account's presence minus its breaks and gaps"
    elif start_fact and end_fact and len(start_fact.values()) == 1 and len(end_fact.values()) == 1:
        for holes_set in break_sets:
            value = creditable_minutes(
                start_fact.values()[0], end_fact.values()[0], list(holes_set)
            )
            if value is not None and value not in minutes:
                minutes.append(value)
        basis = "documented arrival and departure minus documented breaks"
    elif stated_fact:
        minutes = [float(v) for v in stated_fact.values()]
        basis = "stated duration (no complete presence times)"
    if not any(acc["holes"] for acc in alive):
        for cl in shared.values():
            for break_claim in cl:
                used_breaks[break_claim.value].append(break_claim)

    break_facts = []
    for (bs, be), claims in sorted(used_breaks.items()):
        docs = {c.obs.doc for c in claims if not c.copy}
        fact = Fact(
            id=fact_id(event.id, f"break {bs}-{be}"),
            subject=event.id,
            field="break",
            value=[bs, be],
            status="conflicting"
            if len(break_sets) > 1
            else "corroborated"
            if len(docs) > 1
            else "documented",
            rule="documented_non_service_time",
            reason="Non-service time documented for this encounter; subtracted from presence."
            + (" Break accounts disagree; each is a scenario." if len(break_sets) > 1 else ""),
            valid_time=day,
            evidence=[
                Evidence(observation=c.obs.id, block=b, quote=q, value=[bs, be])
                for c in claims
                for b, q in c.blocks
            ],
        )
        facts.append(fact)
        break_facts.append(fact)

    inputs = (
        [f for f in (start_fact, end_fact) if f]
        if (alive or basis.startswith("documented"))
        else ([stated_fact] if stated_fact else [])
    )
    if stated_fact and alive:
        extra = [float(v) for v in stated_fact.values() if float(v) not in minutes]
        if extra:
            open_items.append(
                OpenItem(
                    kind="conflict",
                    subject=event.id,
                    text=f"{event.id}: stated duration {extra} differs from times ({minutes})",
                    blocks=sorted({e.block for e in stated_fact.evidence}),
                    facts=[stated_fact.id],
                )
            )
            minutes += extra
    if minutes:
        conflicting = len(minutes) > 1
        statuses = {f.status for f in inputs}
        status = (
            "conflicting"
            if conflicting
            else "established"
            if "established" in statuses
            else "corroborated"
            if statuses == {"corroborated"}
            else "documented"
        )
        facts.append(
            Fact(
                id=fact_id(event.id, "minutes"),
                subject=event.id,
                field="minutes",
                value=None if conflicting else minutes[0],
                scenarios=sorted(minutes) if conflicting else [],
                status=status,
                rule="computed",
                reason=f"Creditable minutes = {basis}; inputs: "
                + ", ".join(f"{f.field} ({f.status})" for f in inputs + break_facts),
                valid_time=day,
                evidence=[
                    e
                    for f in inputs + break_facts
                    for e in f.evidence
                    if e.stance in {"supports", "copy"}
                ],
            )
        )
    elif start_fact and end_fact:
        open_items.append(
            OpenItem(
                kind="missing",
                subject=event.id,
                text=f"{event.id}: no single record gives both an arrival and a later departure "
                "(they come from different records, or the departure is not after the arrival), so "
                "no duration is computed",
                blocks=sorted({e.block for f in (start_fact, end_fact) for e in f.evidence}),
                facts=[start_fact.id, end_fact.id],
            )
        )

    # documented session time regardless of who was present (clinician or partner time too),
    # per document account; distinct results are scenarios
    session: list[float] = []
    session_evidence: list[Evidence] = []
    for obs in by_doc.values():
        spans: list[tuple[str, str, Observation]] = [
            (str(o.get("start")), str(o.get("end")), o)
            for o in obs
            if o.get("start")
            and o.get("end")
            and (o.get("role") or "presence") not in {"scheduled", "break", "gap"}
            and policy.admits("presence_start", o.evidence_kind)
        ]
        if not spans:
            continue
        first = min(spans, key=lambda x: clock(x[0]))
        last = max(spans, key=lambda x: clock(x[1]))
        # an account whose start or end a correction replaced does not give a session length
        # either (a corrected departure time is not a second scenario)
        if any(
            f is not None
            and f.rule == "signed_correction_supersedes_original"
            and value not in f.values()
            for f, value in ((start_fact, first[0]), (end_fact, last[1]))
        ):
            continue
        gaps = [
            (str(o.get("start")), str(o.get("end")))
            for o in obs
            if o.get("role") in {"break", "gap"} and o.get("start") and o.get("end")
        ]
        value = creditable_minutes(first[0], last[1], gaps)
        if value is not None and value not in session:
            session.append(value)
        for _s, _e, o in (first, last):
            for g in (o.field("start"), o.field("end")):
                if g:
                    session_evidence.append(
                        Evidence(observation=o.id, block=g.block, quote=g.quote, value=value)
                    )
    if session:
        facts.append(
            Fact(
                id=fact_id(event.id, "session_minutes"),
                subject=event.id,
                field="session_minutes",
                value=None if len(session) > 1 else session[0],
                scenarios=sorted(session) if len(session) > 1 else [],
                status="conflicting" if len(session) > 1 else "documented",
                rule="computed",
                reason="Documented session time whoever was present (clinician, partner or patient), "
                "minus breaks and gaps; not the patient's creditable time.",
                valid_time=day,
                evidence=session_evidence,
            )
        )

    # disposition: counts toward the goal only when attended and the service is eligible
    service_fact = next((f for f in facts if f.field == "service"), None)
    service_values = service_fact.values() if service_fact else []
    if service_values and all(s in policy.not_care for s in service_values):
        disposition, why = "not_care", "record handling, not a care contact"
    elif attended and attended.status != "conflicting" and attended.value == "attended":
        if not eligible:
            disposition, why = (
                "attended_no_goal",
                "attended; no documented care goal says which services count",
            )
        elif service_values and all(s in eligible for s in service_values):
            disposition, why = "included", "attended; service counts toward the documented goal"
        elif service_values and not any(s in eligible for s in service_values):
            disposition, why = (
                "excluded",
                f"service {'/'.join(map(str, service_values))} does not count toward the goal",
            )
        else:
            disposition, why = "uncertain", "service type is conflicting"
    elif attended and attended.status != "conflicting":
        disposition, why = "excluded", "patient did not attend"
    elif all(
        not policy.admits("attendance", o.evidence_kind)
        or (
            o.kind == "contact"
            and o.get("status_claim") in {None, "scheduled", "unknown"}
            and not o.get("patient_present")
        )
        or o.kind == "interval"
        for o in members
    ):
        disposition, why = (
            "no_actual_record",
            "only a booking, template, charge or reference; nothing documents what happened",
        )
    else:
        disposition, why = "uncertain", "attendance is not established"
    facts.append(
        Fact(
            id=fact_id(event.id, "disposition"),
            subject=event.id,
            field="disposition",
            value=disposition,
            status="established"
            if disposition != "uncertain"
            else "conflicting"
            if attended and attended.status == "conflicting"
            else "not_documented",
            rule="computed",
            reason=why,
            valid_time=day,
            evidence=[
                e
                for f in (attended, service_fact)
                if f
                for e in f.evidence
                if e.stance == "supports"
            ],
        )
    )
    if disposition == "included" and not minutes:
        facts.append(
            Fact(
                id=fact_id(event.id, "minutes"),
                subject=event.id,
                field="minutes",
                status="not_documented",
                rule="expected_field_missing",
                reason="Attended encounter with no documented presence times or duration.",
                valid_time=day,
            )
        )
        open_items.append(
            OpenItem(
                kind="missing",
                subject=event.id,
                text=f"{event.id}: attended but no documented duration or presence times",
                facts=[fact_id(event.id, "minutes")],
            )
        )
    return facts
