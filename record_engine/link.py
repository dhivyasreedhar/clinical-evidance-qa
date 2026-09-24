"""④ Link (code): observations → events, and copy detection.

- Explicit key: the same encounter/appointment/form identifier from the same issuer is one event.
- Weighted match when no identifier is present, with hand-set weights from policy.toml (not
  estimated from data): the date must match;
  service, time overlap (Allen: equal/overlap/during), participants and issuer add weight. At or
  above T_link the observation joins the event; between T_candidate and T_link it stays separate
  and a candidate link is reported; below, it stays separate. Every link keeps its weights.
- Copies: an observation whose document says it is a copy (relation copy_of), or a document whose
  text is nearly identical to an earlier one (shingle Jaccard), never counts as independent.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from record_engine.ingest import Document
from record_engine.model import Event, Observation, OpenItem
from record_engine.policy import Policy
from record_engine.values import clock

ENCOUNTER_KINDS = {"contact", "interval"}


def norm(text: str | None) -> str:
    return " ".join((text or "").casefold().split())


def id_key(text: str | None) -> str:
    return re.sub(r"[^0-9a-z]", "", (text or "").lower())


class Issuers(dict[str, str]):
    """Document -> issuer, plus the spelling -> organisation map for contact-level issuers."""

    canon: dict[str, str]


# "Organisation | Appointment desk", "Organisation - Scheduling", "Organisation (Front office)":
# the organisation comes first; what follows a separator is a unit within it.
UNIT_SEPARATOR = re.compile(r"\s*(?:\||/|,|\(|\s[-\u2013\u2014]\s)\s*")


def issuer_core(name: str, generic: set[str]) -> str:
    """An issuer's distinctive letters: "LAKESIDE VALLEY HEALTH", "Lakeside Valley",
    "Lakesidevalley" and "Lakeside Valley Health | Front desk" are all "lakesidevalley"
    (generic words such as health or clinic dropped; a unit after a separator is part of the
    organisation before it)."""
    name = UNIT_SEPARATOR.split(name.strip(), maxsplit=1)[0] or name
    words = [w for w in re.findall(r"[a-z0-9]+", name.lower()) if w not in generic]
    return "".join(words) or re.sub(r"[^a-z0-9]", "", name.lower())


def same_issuer(a: str, b: str, generic: set[str]) -> bool:
    ca, cb = issuer_core(a, generic), issuer_core(b, generic)
    return bool(ca) and ca == cb


def doc_issuers(observations: list[Observation], generic: set[str] | None = None) -> Issuers:
    """Each document's issuer, with spellings of one organisation mapped to its most common name
    (so an e-mail signed "Lakesidevalley" is the same issuer as LAKESIDE VALLEY HEALTH)."""
    generic = generic or set()
    stated: dict[str, list[str]] = defaultdict(list)
    for o in observations:
        if o.kind == "doc_meta" and o.get("issuer"):
            name = norm(o.get("issuer"))
            if name not in stated[o.doc]:
                stated[o.doc].append(name)
    counts: dict[str, int] = defaultdict(int)
    for names_of_doc in stated.values():
        for name in names_of_doc:
            counts[name] += 1
    # a document whose header names several issuers (an e-mail signed by a person and sent from an
    # organisation) is issued by the one most documents share
    raw: dict[str, str] = {}
    for doc, names_of_doc in stated.items():
        raw[doc] = max(
            names_of_doc,
            key=lambda n: (
                sum(c for other, c in counts.items() if same_issuer(other, n, generic)),
                -names_of_doc.index(n),
            ),
        )
    names = [n for n in counts if n] + [
        norm(o.get("issuer")) for o in observations if o.get("issuer") and o.kind != "doc_meta"
    ]
    reps: list[str] = []
    canon: dict[str, str] = {}
    for name in sorted(set(names), key=lambda n: (-counts.get(n, 0), n)):
        rep = next((r for r in reps if same_issuer(r, name, generic)), None)
        if rep is None:
            reps.append(name)
            rep = name
        canon[name] = rep
    issuers = Issuers({doc: canon.get(name, name) for doc, name in raw.items()})
    issuers.canon = canon  # contact-level issuers resolve through the same map
    return issuers


def issuer_of(o: Observation, issuers: dict[str, str]) -> str:
    own = norm(o.get("issuer"))
    if own:
        return str(getattr(issuers, "canon", {}).get(own, own))
    return issuers.get(o.doc, "")


# --- copies ----------------------------------------------------------------------------------


def shingles(text: str, size: int) -> set[tuple[str, ...]]:
    words = re.findall(r"\w+", text.lower())
    return {tuple(words[i : i + size]) for i in range(max(0, len(words) - size + 1))}


def detect_copies(
    documents: list[Document], observations: list[Observation], policy: Policy
) -> tuple[dict[str, str], set[str]]:
    """(copy document -> original document by text similarity, copy observation IDs)."""
    size, threshold = policy.link["shingle"], policy.link["copy_jaccard"]
    sets = {d.key: shingles("\n".join(d.lines), size) for d in documents}
    first_recorded: dict[str, str] = {}
    for o in observations:
        for r in o.recorded:
            if o.doc not in first_recorded or r.value < first_recorded[o.doc]:
                first_recorded[o.doc] = r.value
    copies: dict[str, str] = {}
    keys = sorted(sets)
    for i, a in enumerate(keys):
        for b in keys[i + 1 :]:
            union = sets[a] | sets[b]
            if not union:
                continue
            if len(sets[a] & sets[b]) / len(union) >= threshold:
                # the later-recorded document is the copy (ties: the later name, deterministically)
                later, earlier = sorted(
                    (a, b), key=lambda k: (first_recorded.get(k, "9999"), k), reverse=True
                )
                copies[later] = earlier
    copy_obs = {o.id for o in observations if o.relation.type == "copy_of" or o.doc in copies}
    return copies, copy_obs


# --- events ----------------------------------------------------------------------------------


class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)


def span(o: Observation) -> tuple[int, int] | None:
    s, e = o.get("start"), o.get("end")
    return (clock(s), clock(e)) if s and e else None


def match_score(
    o: Observation, other: list[Observation], policy: Policy, issuers: dict[str, str]
) -> tuple[float, dict[str, float]]:
    """Hand-weighted evidence that an unkeyed contact is the same event as a group of observations."""
    weights = policy.link["weights"]
    parts: dict[str, float] = {}
    date = o.get("date")
    if not date or all(x.get("date") != date for x in other):
        return 0.0, {"date": 0.0}
    parts["date"] = weights.get("date", 0.0)
    service = policy.categories(o.get("service"))
    if service and any(policy.categories(x.get("service")) & service for x in other):
        parts["service"] = weights["service"]
    mine = span(o)
    if mine:
        best = 0.0
        for x in other:
            theirs = span(x)
            if not theirs:
                continue
            if theirs == mine:
                best = max(best, weights["time_equal"])
            elif mine[0] < theirs[1] and theirs[0] < mine[1]:
                best = max(best, weights["time_overlap"])
        if best:
            parts["time"] = best
    people = set(re.findall(r"[a-z]{3,}", norm(o.get("participants"))))
    if people and any(
        people & set(re.findall(r"[a-z]{3,}", norm(x.get("participants")))) for x in other
    ):
        parts["participants"] = weights["participants"]
    if issuer_of(o, issuers) and any(issuer_of(x, issuers) == issuer_of(o, issuers) for x in other):
        parts["issuer"] = weights["issuer"]
    return round(sum(parts.values()), 3), parts


def link(
    observations: list[Observation], policy: Policy
) -> tuple[list[Event], dict[str, str], list[OpenItem]]:
    """Events, observation -> event ID, and candidate-link open items."""
    issuers = doc_issuers(observations, set(policy.link.get("issuer_generic_words", [])))
    uf = UnionFind()
    event_of: dict[str, str] = {}
    keys_of: dict[str, set[str]] = defaultdict(set)
    open_items: list[OpenItem] = []

    # 1. explicit identifiers (encounter and appointment IDs share one namespace per issuer)
    encounter_obs = [o for o in observations if o.kind in ENCOUNTER_KINDS]
    namespaces: dict[str, set[str]] = defaultdict(set)  # identifier -> issuers that use it
    for o in encounter_obs:
        issuer = issuer_of(o, issuers)
        if issuer:
            for f in ("encounter_id", "appointment_id"):
                if o.get(f):
                    namespaces[id_key(o.get(f))].add(issuer)
    unconfirmed: set[str] = set()
    for o in encounter_obs:
        ids = [id_key(o.get(f)) for f in ("encounter_id", "appointment_id") if o.get(f)]
        issuer = issuer_of(o, issuers)
        for i in ids:
            # a record that names no issuer joins the one issuer that uses this identifier;
            # if several issuers use it, it stays in its own (unknown) namespace
            if not issuer and len(namespaces.get(i, set())) == 1:
                issuer = next(iter(namespaces[i]))
                unconfirmed.add(o.id)
            node = f"id:{issuer}|{i}"
            uf.union(f"obs:{o.id}", node)
            keys_of[f"obs:{o.id}"].add(o.get("encounter_id") or o.get("appointment_id") or i)

    # 2. intervals without an identifier belong to their document's contact on the same date
    by_doc: dict[str, list[Observation]] = defaultdict(list)
    for o in encounter_obs:
        by_doc[o.doc].append(o)
    for o in encounter_obs:
        if o.kind != "interval" or o.get("encounter_id"):
            continue
        contacts = [c for c in by_doc[o.doc] if c.kind == "contact"]
        same_day = [c for c in contacts if not o.get("date") or c.get("date") == o.get("date")]
        if len(same_day) == 1:
            uf.union(f"obs:{o.id}", f"obs:{same_day[0].id}")

    # 2b. an unnumbered observation in a document whose other encounter observations all belong
    # to one event (a second mention of the same visit) joins that event when dates agree
    for obs in by_doc.values():
        keyed_roots = {
            uf.find(f"obs:{o.id}") for o in obs if o.get("encounter_id") or o.get("appointment_id")
        }
        if len(keyed_roots) != 1:
            continue
        root = next(iter(keyed_roots))
        days = {o.get("date") for o in obs if uf.find(f"obs:{o.id}") == root and o.get("date")}
        members = [o for o in obs if uf.find(f"obs:{o.id}") == root]
        services = set().union(
            *(policy.categories(o.get("service")) for o in members if o.get("service"))
        )
        spans = [sp for o in members if (sp := span(o))]
        for o in obs:
            if o.get("encounter_id") or o.get("appointment_id"):
                continue
            if o.get("date") and o.get("date") not in days:
                continue
            # a different kind of contact (a follow-up call about a missed visit) stays separate:
            # it joins only when its service and time are compatible with the visit
            mine = policy.categories(o.get("service")) if o.get("service") else set()
            if mine and services and not (mine & services):
                continue
            own = span(o)
            if own and spans and not any(own[0] < b and a < own[1] for a, b in spans):
                continue
            uf.union(f"obs:{o.id}", root)

    # 3. weighted match for contacts that carry no identifier
    groups: dict[str, list[Observation]] = defaultdict(list)
    for o in encounter_obs:
        groups[uf.find(f"obs:{o.id}")].append(o)
    link_info: dict[str, dict[str, Any]] = {}
    candidates: list[tuple[Observation, str, float, dict[str, float]]] = []
    for o in encounter_obs:
        if o.kind != "contact" or o.get("encounter_id") or o.get("appointment_id"):
            continue
        root = uf.find(f"obs:{o.id}")
        best: tuple[float, str, dict[str, float]] = (0.0, "", {})
        for other_root, members in groups.items():
            if other_root == root or any(m.doc == o.doc for m in members):
                continue
            score, parts = match_score(o, members, policy, issuers)
            if score > best[0]:
                best = (score, other_root, parts)
        score, target, parts = best
        if score >= policy.link["T_link"]:
            uf.union(root, target)
            link_info[o.id] = {"linked_by": "weighted", "score": score, "weights": parts}
        elif score >= policy.link["T_candidate"]:
            candidates.append((o, target, score, parts))

    # 4. assemble encounter events
    assembled: dict[str, list[Observation]] = defaultdict(list)
    for o in encounter_obs:
        assembled[uf.find(f"obs:{o.id}")].append(o)
    events: list[Event] = []
    pending: list[tuple[str, list[Observation], list[str], dict[str, Any]]] = []
    for n, (_root, group) in enumerate(
        sorted(assembled.items(), key=lambda kv: min(o.get("date") or "9" for o in kv[1]))
    ):
        names = sorted({k for o in group for k in keys_of.get(f"obs:{o.id}", set())})
        encounter_ids = sorted({str(o.get("encounter_id")) for o in group if o.get("encounter_id")})
        if encounter_ids:
            event_id = encounter_ids[0]
        elif names:
            event_id = names[0]
        else:
            # no identifier anywhere: a short readable label from what the record says about it
            # (the service category, else how the contact happened)
            service = next(
                (
                    label
                    for o in group
                    if o.get("service")
                    and (label := policy.service(o.get("service"))) in policy.services["order"]
                ),
                None,
            ) or next((str(o.get("mode")).lower() for o in group if o.get("mode")), None)
            day = next((o.get("date") for o in group if o.get("date")), None)
            if day is None:
                # the date the contact's document gives all its dated contacts, if only one
                doc_days = {x.get("date") for x in by_doc.get(group[0].doc, []) if x.get("date")}
                day = next(iter(doc_days)) if len(doc_days) == 1 else None
            event_id = (
                f"unnumbered {(service + ' ') if service else ''}contact on "
                f"{day or 'an undated day'} ({group[0].doc})"
            )
            if any(p[0] == event_id for p in pending):
                event_id += f" #{n}"
        if len(encounter_ids) > 1:
            event_id = "+".join(encounter_ids)
        info: dict[str, Any] = {"linked_by": "identifier" if names else "document"}
        info.update({o.id: link_info[o.id] for o in group if o.id in link_info})
        if any(o.id in unconfirmed for o in group):
            info["issuer_unconfirmed"] = sorted(o.id for o in group if o.id in unconfirmed)
        pending.append((event_id, group, names, info))
    # One identifier used by two issuers names two different events. The issuer most documents
    # come from keeps the plain identifier; the other is qualified by its issuer, so their facts
    # never share an ID.
    doc_issuer_counts: dict[str, int] = defaultdict(int)
    for value in issuers.values():
        doc_issuer_counts[value] += 1
    primary = max(doc_issuer_counts, key=lambda k: (doc_issuer_counts[k], k), default="")

    # a correction names the record it corrects: when its only difference is the issuer written on
    # it (a person's signature, another spelling), it joins that record instead of starting one
    def is_correction(group: list[Observation]) -> bool:
        keyed = [o for o in group if o.get("encounter_id") or o.get("appointment_id")]
        return bool(keyed) and all(
            o.relation.type == "corrects"
            or (o.relation.type == "addendum" and bool(o.relation.fields))
            for o in keyed
        )

    merged: list[tuple[str, list[Observation], list[str], dict[str, Any]]] = []
    for entry in pending:
        into = next(
            (
                m
                for m in merged
                if m[0] == entry[0] and (is_correction(entry[1]) or is_correction(m[1]))
            ),
            None,
        )
        if into is None:
            merged.append(entry)
            continue
        keep_entry, joining = (into, entry) if not is_correction(into[1]) else (entry, into)
        joined = (
            keep_entry[0],
            keep_entry[1] + joining[1],
            keep_entry[2],
            {**joining[3], **keep_entry[3]},
        )
        merged[merged.index(into)] = joined
    pending = merged
    taken: dict[str, int] = defaultdict(int)
    for event_id, *_ in pending:
        taken[event_id] += 1
    for event_id, group, names, info in pending:
        if taken[event_id] > 1:
            keyed = [
                issuer_of(o, issuers)
                for o in group
                if o.get("encounter_id") or o.get("appointment_id")
            ]
            issuer = max(set(keyed), key=keyed.count) if keyed else ""
            if issuer and issuer != primary:
                info["qualified_by_issuer"] = issuer
                event_id = f"{event_id}@{issuer.replace(' ', '-')}"
        events.append(
            Event(
                id=event_id,
                kind="encounter",
                observations=[o.id for o in group],
                keys=names,
                link=info,
            )
        )
        for o in group:
            event_of[o.id] = event_id
    # candidate links name both events, so a reference can say which visit it probably is
    root_event = {uf.find(f"obs:{o.id}"): event_of[o.id] for o in encounter_obs}
    for o, target, score, parts in candidates:
        event_name = event_of[o.id]
        other_event = root_event.get(uf.find(target), "another record")
        open_items.append(
            OpenItem(
                kind="candidate_link",
                subject=event_name,
                text=f"{event_name} may be the same event as {other_event} (weighted match {score}: "
                f"{', '.join(parts)}); kept separate",
                blocks=o.blocks,
                facts=[other_event],
            )
        )

    # 5. other kinds: measurements by instrument + form/date, goals by target, others one each
    other: dict[tuple[str, ...], list[Observation]] = defaultdict(list)
    for o in observations:
        if o.kind in ENCOUNTER_KINDS:
            continue
        if o.kind == "measurement":
            key: tuple[str, ...] = (
                "measurement",
                id_key(o.get("instrument")),
                id_key(o.get("item")),
                id_key(o.get("form_id")) or (o.get("completed_on") or o.id),
            )
        elif o.kind == "plan_goal":
            # a goal restated by several documents is one goal; the same target with another
            # effective start is another goal (a later plan), reconciled by goal supersession
            key = (
                "goal",
                norm(o.get("unit")),
                norm(o.get("period")),
                norm(o.get("target")),
                o.get("effective_start") or "",
            )
        elif o.kind == "medication":
            key = (
                "medication",
                id_key(o.get("name")),
                o.get("date") or "",
                o.get("change") or "",
                o.doc,
            )
        elif o.kind == "charge":
            key = ("charge", id_key(o.get("charge_id")) or o.id)
        elif o.kind == "doc_meta":
            key = ("document", o.doc)
        else:
            key = (o.kind, o.id)
        other[key].append(o)
    # a measurement recorded with a form ID and the same administration recorded by date only
    for key, group in list(other.items()):
        if key[0] != "measurement" or not group[0].get("form_id"):
            continue
        dated = {o.get("completed_on") for o in group if o.get("completed_on")}
        for other_key in list(other):
            if other_key[:3] == key[:3] and other_key != key and other_key[3] in dated:
                group.extend(other.pop(other_key))

    # form IDs are numbered by whichever system imported the form: the same instrument completed
    # on the same day with the same score under another form ID is the same administration
    # (a re-import); a different score on that day is a second administration
    def administration(group: list[Observation]) -> tuple[str, ...] | None:
        o = group[0]
        scores = {str(x.get("score")) for x in group if x.get("score") is not None}
        if not o.get("completed_on") or len(scores) != 1:
            return None
        return (
            id_key(o.get("instrument")),
            id_key(o.get("item")),
            str(o.get("completed_on")),
            *scores,
        )

    first_with: dict[tuple[str, ...], tuple[str, ...]] = {}
    for key in [k for k in other if k[0] == "measurement"]:
        same = administration(other[key])
        if same is None or key not in other:
            continue
        if same not in first_with:
            first_with[same] = key
            continue
        kept = first_with[same]
        ids = sorted({str(o.get("form_id")) for o in other[kept] + other[key] if o.get("form_id")})
        moved = other.pop(key)
        other[kept].extend(moved)
        if len(ids) > 1:
            open_items.append(
                OpenItem(
                    kind="candidate_link",
                    subject=f"M:{moved[0].get('instrument')} {same[2]}",
                    text=f"{moved[0].get('instrument')} completed {same[2]} (score {same[3]}) is "
                    f"recorded under form IDs {', '.join(ids)}; same instrument, date and score, "
                    "so it is treated as one administration",
                    blocks=[b for o in moved for b in o.blocks],
                )
            )
    for key, group in other.items():
        kind = (
            key[0]
            if key[0] in {"measurement", "goal", "medication", "document", "charge"}
            else group[0].kind
        )
        if kind == "measurement":
            o = group[0]
            label = f"{o.get('instrument')}{' item ' + str(o.get('item')) if o.get('item') else ''} {o.get('completed_on') or o.get('form_id') or ''}".strip()
            event_id = f"M:{label}"
            # two administrations on one day are two events, told apart by form ID
            if any(e.id == event_id for e in events):
                event_id += f" ({o.get('form_id') or o.id})"
        elif kind == "goal":
            event_id = f"G:{key[3] or key[1]}"
            if any(e.id == event_id for e in events) or any(
                k[0] == "goal" and k[1:4] == key[1:4] and k != key for k in other
            ):
                event_id += f" from {key[4] or 'undated'}"
        elif kind == "document":
            event_id = f"D:{key[1]}"
        elif kind == "charge":
            first = group[0]
            event_id = f"charge {first.get('charge_id') or first.get('date') or first.id}"
        elif kind == "medication":
            # named by what the record says, so the same decision gets the same ID in every build
            first = group[0]
            event_id = (
                f"medication {first.get('name') or 'unnamed'} {first.get('change') or ''} "
                f"{first.get('date') or 'undated'} ({first.doc})"
            ).replace("  ", " ")
            if any(e.id == event_id for e in events):
                event_id += f" #{sum(e.id.startswith(event_id) for e in events) + 1}"
        else:
            event_id = f"{kind[:3].upper()}:{group[0].id}"
        events.append(Event(id=event_id, kind=kind, observations=[o.id for o in group]))
        for o in group:
            event_of[o.id] = event_id
    return events, event_of, open_items
