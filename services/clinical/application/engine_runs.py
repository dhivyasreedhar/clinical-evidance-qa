"""Record engine runs: build a patient's record with ``record_engine`` and answer questions over it.

Runs are durable tasks (``analysis_tasks``) of two kinds: ``engine_record`` builds the record from
a snapshot's documents (extraction, linking, reconciliation), and ``engine_answer`` answers one
question over a finished record. Results are stored in ``analysis_results``. Model calls run
outside database transactions; the task lease is re-checked before the result is written.
"""

import hashlib
import json
import re
import threading
from collections import defaultdict
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Engine, or_, select, text
from sqlalchemy.orm import Session

from clinical.application.imports import IdempotencyConflict, NotFound, require_patient
from clinical.infrastructure.config import Settings
from clinical.infrastructure.database import transaction
from clinical.infrastructure.models import (
    AnalysisResult,
    AnalysisTask,
    AuditEvent,
    Job,
    Patient,
    Revision,
    Snapshot,
    SourceSpan,
)
from record_engine import VERSION as ENGINE_VERSION
from record_engine import llm
from record_engine import query as dsl
from record_engine.crosscheck import observe_checked
from record_engine.evidence import PassageIndex
from record_engine.extract import PROMPT_VERSION as EXTRACT_VERSION
from record_engine.ingest import Document, ingest_text
from record_engine.model import Fact, Record
from record_engine.policy import Policy
from record_engine.policy import load as load_policy
from record_engine.qa import answer_question
from record_engine.reconcile import build_record
from record_engine.render import abstraction_markdown, block_texts, statement_blocks

RECORD, ANSWER = "engine_record", "engine_answer"
KINDS = (RECORD, ANSWER)
WEEKS = (
    "from encounters where disposition = included group_by week "
    "select count(), count_distinct(date), sum(minutes), goal_met()"
)
BLOCK = re.compile(r"^(?P<doc>.+):L(?P<start>\d+)(?:-(?P<end>\d+))?$")
# Event kinds shown with their facts; findings are listed by date instead.
EVENT_KINDS = ("patient", "encounter", "measurement", "medication", "goal", "charge")


class RunError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class RunLease:
    task_id: UUID
    token: UUID


def versions() -> tuple[str, str]:
    """(prompt version, schema version) a task was created with; a task whose versions differ
    from the running engine's is failed rather than processed with other prompts."""
    return f"{ENGINE_VERSION}:{EXTRACT_VERSION}", load_policy().version


def enqueue_run(
    session: Session,
    settings: Settings,
    tenant: UUID,
    actor: UUID,
    patient: UUID,
    key: str,
    snapshot_id: UUID | None = None,
    record_id: UUID | None = None,
    question: str | None = None,
) -> AnalysisTask:
    """Queue a record build (``snapshot_id``) or a question over a finished record
    (``record_id`` + ``question``)."""
    require_patient(session, patient, actor)
    if not settings.anthropic_api_key.get_secret_value():
        raise RunError("claude_key_missing")
    if question is not None:
        base = session.get(AnalysisTask, record_id) if record_id else None
        if not base or base.patient_id != patient or base.kind != RECORD:
            raise NotFound
        if base.status != "succeeded":
            raise RunError("engine_record_required")
        if (base.prompt_version, base.schema_version) != versions():
            raise RunError("record_outdated")
        snapshot_id = base.snapshot_id
        kind = ANSWER
    else:
        if record_id is not None:
            raise RunError("question_required")
        kind = RECORD
    snapshot = session.get(Snapshot, snapshot_id) if snapshot_id else None
    if not snapshot or snapshot.patient_id != patient:
        raise NotFound
    if not snapshot.manifest:
        raise RunError("no_sources")
    prompt_version, schema_version = versions()
    # One active run per patient; idempotency serializes across patients too.
    for value in (f"analysis-key:{tenant}:{actor}:{key}", f"analysis-patient:{tenant}:{patient}"):
        lock = int.from_bytes(hashlib.sha256(value.encode()).digest()[:8], signed=True)
        session.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": lock})
    digest = hashlib.sha256(
        json.dumps(
            [
                kind,
                str(patient),
                str(snapshot.id),
                str(record_id),
                question,
                prompt_version,
                schema_version,
            ]
        ).encode()
    ).hexdigest()
    prior = session.scalar(
        select(AnalysisTask).where(
            AnalysisTask.actor_id == actor, AnalysisTask.idempotency_key == key
        )
    )
    if prior:
        if prior.payload_hash != digest:
            raise IdempotencyConflict
        return prior
    active = session.scalar(
        select(AnalysisTask).where(
            AnalysisTask.patient_id == patient, AnalysisTask.status.in_(["queued", "running"])
        )
    )
    if active:
        if active.payload_hash == digest and active.actor_id == actor:
            return active
        raise RunError("run_already_active")
    task = AnalysisTask(
        tenant_id=tenant,
        patient_id=patient,
        actor_id=actor,
        snapshot_id=snapshot.id,
        abstraction_id=record_id if kind == ANSWER else None,
        question=question,
        kind=kind,
        model=llm.WRITER,
        prompt_version=prompt_version,
        schema_version=schema_version,
        idempotency_key=key,
        payload_hash=digest,
    )
    session.add(task)
    session.flush()
    session.add(
        AuditEvent(
            tenant_id=tenant,
            actor_id=actor,
            patient_id=patient,
            action="analysis.queued",
            resource_id=task.id,
            details={"kind": kind, "snapshot_id": str(snapshot.id)},
        )
    )
    return task


def enqueue_latest_records(engine: Engine, settings: Settings, tenant: UUID) -> None:
    """Build the record for each patient's latest snapshot once per engine version. Unchanged
    documents come from the extraction cache, so a rebuild after an import pays only for the new
    documents."""
    if not settings.anthropic_api_key.get_secret_value():
        return
    prompt_version, schema_version = versions()
    with transaction(engine, tenant) as session:
        # the latest snapshot of every active (not archived) patient
        snapshots = session.scalars(
            select(Snapshot)
            .join(Patient, Patient.id == Snapshot.patient_id)
            .where(Patient.archived.is_(False))
            .distinct(Snapshot.patient_id)
            .order_by(Snapshot.patient_id, Snapshot.sequence.desc())
        ).all()
        for snapshot in snapshots:
            if not snapshot.manifest:
                continue  # every document was withdrawn; there is nothing to build
            existing = session.scalar(
                select(AnalysisTask.id)
                .where(
                    AnalysisTask.patient_id == snapshot.patient_id,
                    AnalysisTask.kind == RECORD,
                    AnalysisTask.snapshot_id == snapshot.id,
                    # a record built by another engine version is rebuilt once
                    AnalysisTask.prompt_version == prompt_version,
                    AnalysisTask.schema_version == schema_version,
                )
                .limit(1)
            )
            if existing:
                continue  # failures need an explicit retry, never an automatic paid loop
            job = session.scalar(
                select(Job)
                .where(Job.patient_id == snapshot.patient_id, Job.status == "succeeded")
                .order_by(Job.created_at.desc())
                .limit(1)
            )
            if not job:
                continue
            try:
                enqueue_run(
                    session,
                    settings,
                    tenant,
                    job.actor_id,
                    snapshot.patient_id,
                    f"auto-record:{snapshot.id}:{prompt_version}:{schema_version}",
                    snapshot_id=snapshot.id,
                )
            except NotFound:
                continue  # the importing user no longer has access to this patient
            except RunError as error:
                if error.code != "run_already_active":
                    raise


def claim_run(engine: Engine, tenant: UUID, lease_seconds: int = 120) -> RunLease | None:
    with transaction(engine, tenant) as session:
        now = datetime.now(UTC)
        task = session.scalar(
            select(AnalysisTask)
            .where(
                or_(
                    AnalysisTask.status == "queued",
                    (AnalysisTask.status == "running") & (AnalysisTask.lease_until < now),
                )
            )
            .order_by(AnalysisTask.created_at)
            .with_for_update(skip_locked=True)
            .limit(1)
        )
        if not task:
            return None
        if task.attempt >= 2:
            task.status, task.error_code, task.finished_at = "failed", "run_lease_exhausted", now
            return None
        task.status, task.attempt = "running", task.attempt + 1
        task.error_code, task.finished_at = None, None
        task.lease_token, task.lease_until = uuid4(), now + timedelta(seconds=lease_seconds)
        return RunLease(task.id, task.lease_token)


def renew_lease(engine: Engine, tenant: UUID, lease: RunLease, seconds: int) -> bool:
    """Extend a held lease; False once it is lost (expired, released or taken over)."""
    with transaction(engine, tenant) as session:
        task = valid_run(session, lease)
        if task is None:
            return False
        task.lease_until = datetime.now(UTC) + timedelta(seconds=seconds)
        return True


@contextmanager
def kept_lease(engine: Engine, tenant: UUID, lease: RunLease, seconds: int) -> Iterator[None]:
    """Renew the lease while the model steps run, so a worker that stops (a restart, a crash)
    loses its runs after one short lease and another worker resumes them from the model cache,
    instead of the run looking busy for the length of a whole build."""
    done = threading.Event()

    def beat() -> None:
        while not done.wait(seconds / 4):
            try:
                if not renew_lease(engine, tenant, lease, seconds):
                    return
            except Exception:  # a failed renewal is retried; the lease fences the result
                continue

    thread = threading.Thread(target=beat, name="lease", daemon=True)
    thread.start()
    try:
        yield
    finally:
        done.set()
        thread.join()


def release_run(engine: Engine, tenant: UUID, lease: RunLease) -> None:
    """Hand an unfinished run back to the queue (the worker is stopping). It is not counted as
    an attempt, and the stopped worker can no longer write its result."""
    with transaction(engine, tenant) as session:
        task = valid_run(session, lease)
        if task is None:
            return
        task.status, task.lease_token, task.lease_until = "queued", None, None
        task.attempt = max(0, task.attempt - 1)


def valid_run(session: Session, lease: RunLease) -> AnalysisTask | None:
    task = session.scalar(
        select(AnalysisTask).where(AnalysisTask.id == lease.task_id).with_for_update()
    )
    if (
        not task
        or task.status != "running"
        or task.lease_token != lease.token
        or not task.lease_until
        or task.lease_until <= datetime.now(UTC)
    ):
        return None
    return task


def snapshot_documents(
    session: Session, snapshot: Snapshot
) -> tuple[list[Document], dict[str, UUID]]:
    """The snapshot's revisions as engine documents (integrity checked), and document key ->
    revision ID. Keys are file stems, made unique when two revisions share a file name."""
    manifest = {item["revision_id"]: item["sha256"] for item in snapshot.manifest}
    revisions = session.scalars(
        select(Revision)
        .where(Revision.id.in_([UUID(i) for i in manifest]))
        .order_by(Revision.filename, Revision.id)
    ).all()
    if len(revisions) != len(manifest):
        raise RunError("source_manifest_incomplete")
    documents: list[Document] = []
    keys: dict[str, UUID] = {}
    for revision in revisions:
        digest = hashlib.sha256(revision.text.encode("utf-8")).hexdigest()
        if revision.sha256 != manifest[str(revision.id)] or digest != revision.sha256:
            raise RunError("source_integrity_failed")
        stem = revision.filename.rsplit(".", 1)[0]
        name = f"{stem}~{len(keys)}.txt" if stem in keys else revision.filename
        document = ingest_text(name, revision.text)
        documents.append(document)
        keys[document.key] = revision.id
    return documents, keys


class Citations:
    """Engine line ranges (``doc:Lx-y``) resolved to the snapshot's source spans."""

    def __init__(self, session: Session, keys: dict[str, UUID]):
        self.keys = keys
        revisions = list(keys.values())
        self.filenames = {
            r.id: r.filename
            for r in session.scalars(select(Revision).where(Revision.id.in_(revisions)))
        }
        self.spans: dict[UUID, list[SourceSpan]] = defaultdict(list)
        for span in session.scalars(
            select(SourceSpan)
            .where(SourceSpan.revision_id.in_(revisions))
            .order_by(SourceSpan.revision_id, SourceSpan.ordinal)
        ):
            self.spans[span.revision_id].append(span)

    def __call__(self, blocks: Iterable[str], limit: int | None = None) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        seen: set[UUID] = set()
        for block in blocks:
            m = BLOCK.match(block)
            if not m or m.group("doc") not in self.keys:
                continue
            revision = self.keys[m.group("doc")]
            start = int(m.group("start"))
            end = int(m.group("end") or start)
            for span in self.spans[revision]:
                if span.start_line <= end and span.end_line >= start and span.id not in seen:
                    seen.add(span.id)
                    out.append(
                        {
                            "span_id": str(span.id),
                            "revision_id": str(revision),
                            "filename": self.filenames[revision],
                            "start_line": span.start_line,
                            "end_line": span.end_line,
                            "quote": span.quote,
                        }
                    )
                    if limit and len(out) >= limit:
                        return out
        return out


def values_of(value: Any) -> list[Any]:
    """A plain value or a set of scenarios, as a list of the possible values."""
    if isinstance(value, dict) and "scenarios" in value:
        return list(value["scenarios"])
    return [] if value is None else [value]


def jsonable(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str))


def record_view(
    record: Record, policy: Policy, cite: Citations, keys: dict[str, UUID]
) -> dict[str, Any]:
    """What the workspace shows: the encounter ledger, weekly goal results and totals (all
    computed by code), each event's facts, findings by date, the documents and open items, with
    every value linked to its source spans."""
    facts_by_subject: dict[str, list[Fact]] = defaultdict(list)
    for fact in record.facts:
        facts_by_subject[fact.subject].append(fact)

    def event_blocks(event_id: str) -> list[str]:
        return [e.block for f in facts_by_subject[event_id] for e in f.evidence]

    rows = dsl.execute(dsl.parse("from encounters select rows()"), record, policy)["rows"]
    encounters = [
        {
            "id": r["id"],
            "date": r.get("date"),
            "weekday": r.get("weekday"),
            "service": r.get("service"),
            "attendance": r.get("attendance"),
            "disposition": r.get("disposition"),
            "minutes": values_of(r.get("minutes")),
            "status": r.get("status"),
            "reason": r.get("status_reason"),
            "citations": cite(event_blocks(r["id"]), limit=12),
        }
        for r in (rows[0]["rows()"] if rows else [])
    ]
    weeks = []
    totals = None
    for w in dsl.execute(dsl.parse(WEEKS), record, policy)["rows"]:
        entry = {
            "week": w["group"],
            "partial": bool(w.get("partial_week")),
            "sessions": w.get("count()"),
            "days": w.get("count_distinct(date)"),
            "minutes": values_of(w.get("sum(minutes)")),
        }
        if w["group"] == "all groups":
            totals = entry
            continue
        goal = w.get("goal_met()") or {}
        weeks.append(
            {
                **entry,
                "goal": goal.get("status"),
                "thresholds": [
                    {
                        "threshold": t["threshold"],
                        "measured": t["measured"],
                        "outcome": t["outcome"],
                    }
                    for t in goal.get("by_threshold", [])
                ],
            }
        )
    kinds = {e.id: e.kind for e in record.events}
    events = [
        {
            "id": e.id,
            "kind": e.kind,
            "facts": [
                {
                    "field": f.field,
                    "values": f.values(),
                    "status": f.status,
                    "reason": f.reason,
                    "citations": cite([x.block for x in f.evidence], limit=4),
                }
                for f in facts_by_subject[e.id]
            ],
        }
        for e in record.events
        if e.kind in EVENT_KINDS
    ]
    findings = []
    for e in record.events:
        if e.kind != "finding":
            continue
        fields = {f.field: f for f in facts_by_subject[e.id]}
        if "text" not in fields:
            continue
        findings.append(
            {
                "id": e.id,
                "date": fields["date"].value if "date" in fields else None,
                "type": fields["type"].value if "type" in fields else None,
                "reporter": fields["reporter"].value if "reporter" in fields else None,
                "text": fields["text"].value,
                "status": fields["text"].status,
                "citations": cite(event_blocks(e.id), limit=4),
            }
        )
    findings.sort(key=lambda f: (str(f["date"] or ""), str(f["id"])))
    # the service dates each document supports, from the encounters its evidence belongs to
    dates: dict[str, set[str]] = defaultdict(set)
    for fact in record.facts:
        if kinds.get(fact.subject) == "encounter" and fact.field == "date" and fact.value:
            for evidence in fact.evidence:
                dates[evidence.block.split(":L", 1)[0]].add(str(fact.value))
    documents = [
        {
            "key": d["key"],
            "revision_id": str(keys[d["key"]]) if d["key"] in keys else None,
            "filename": d["filename"],
            "title": d.get("title"),
            "issuer": d.get("issuer"),
            "copy_of": d.get("copy_of"),
            "set_aside": d.get("set_aside"),
            "service_dates": sorted(dates[d["key"]]),
        }
        for d in record.documents
    ]
    documents.sort(key=lambda d: (d["service_dates"][:1] or ["9999"], d["filename"]))
    view: dict[str, Any] = jsonable(
        {
            "events_total": len(record.events),
            "facts_total": len(record.facts),
            "encounters": encounters,
            "weeks": weeks,
            "totals": totals,
            "events": events,
            "findings": findings,
            "documents": documents,
            "open_items": [
                {
                    "kind": o.kind,
                    "subject": o.subject,
                    "text": o.text,
                    "citations": cite(o.blocks, limit=6),
                }
                for o in record.open_items
            ],
        }
    )
    return view


def with_citations(
    answer: dict[str, Any], record: Record, documents: list[Document], cite: Citations
) -> dict[str, Any]:
    """The published answer with each statement's evidence resolved to source spans; internal
    query results and model check details are not kept."""
    facts = {f.id: f for f in record.facts}
    texts = block_texts(documents)
    published = answer.get("status") != "withheld"
    body = answer.get("answer") or {}

    def resolved(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        out = []
        for s in items if published else []:
            groups = statement_blocks(s, answer.get("results", []), record, facts, texts)
            out.append(
                {
                    "text": s["text"],
                    "kind": s["kind"],
                    "citations": cite(b for bs in groups.values() for b in bs),
                }
            )
        return out

    return {
        "status": answer.get("status"),
        # what answers the question, then checked details it did not ask about (held back)
        "statements": resolved(body.get("statements", [])),
        "omitted": resolved(body.get("omitted", [])),
        "reasons": [str(r) for r in answer.get("reasons", [])],
    }


def process_run(engine: Engine, settings: Settings, tenant: UUID, lease: RunLease) -> None:
    try:
        with transaction(engine, tenant) as session:
            task = valid_run(session, lease)
            if task is None:
                return
            if (task.prompt_version, task.schema_version) != versions():
                raise RunError("engine_version_unavailable")
            require_patient(session, task.patient_id, task.actor_id)
            task.lease_until = datetime.now(UTC) + timedelta(seconds=settings.run_lease_seconds)
            snapshot = session.get(Snapshot, task.snapshot_id)
            if not snapshot:
                raise NotFound
            documents, keys = snapshot_documents(session, snapshot)
            kind, question, task_id = task.kind, task.question, task.id
            base_record: dict[str, Any] | None = None
            if kind == ANSWER:
                base = session.scalar(
                    select(AnalysisResult).where(AnalysisResult.task_id == task.abstraction_id)
                )
                if not base or "record" not in base.data:
                    raise RunError("engine_record_required")
                base_record = base.data["record"]
        # The transaction above is closed before any model call.
        policy = load_policy()
        llm.KEY = settings.anthropic_api_key.get_secret_value()
        answer: dict[str, Any] = {}
        with (
            kept_lease(engine, tenant, lease, settings.run_lease_seconds),
            llm.scope() as usage,
        ):
            if kind == RECORD:
                observations, problems, _report = observe_checked(documents, policy, workers=6)
                record = build_record(documents, observations, policy, problems)
            else:
                record = Record.model_validate(base_record)
                answer = answer_question(
                    str(task_id), question or "", record, policy, PassageIndex(documents)
                )
        spent = usage.as_dict()
        with transaction(engine, tenant) as session:
            task = valid_run(session, lease)
            if task is None:
                return
            require_patient(session, task.patient_id, task.actor_id)
            cite = Citations(session, keys)
            if kind == RECORD:
                data: dict[str, Any] = {
                    "record": record.model_dump(mode="json"),
                    "view": record_view(record, policy, cite, keys),
                    "abstraction_markdown": abstraction_markdown(record, documents),
                }
            else:
                data = {"answer": with_citations(answer, record, documents, cite)}
            session.add(
                AnalysisResult(
                    tenant_id=tenant,
                    patient_id=task.patient_id,
                    task_id=task.id,
                    data=jsonable(data),
                    usage={
                        "model": task.model,
                        "input_tokens": spent["input_tokens"],
                        "output_tokens": spent["output_tokens"],
                        "cost_usd": spent["cost_usd"],
                        "calls": spent["calls"],
                        "cached_calls": spent["cached"],
                    },
                )
            )
            task.status, task.finished_at = "succeeded", datetime.now(UTC)
            session.add(
                AuditEvent(
                    tenant_id=tenant,
                    actor_id=task.actor_id,
                    patient_id=task.patient_id,
                    action="analysis.completed",
                    resource_id=task.id,
                    details={"kind": kind, "cost_usd": spent["cost_usd"]},
                )
            )
    except Exception as exc:
        code = exc.code if isinstance(exc, RunError) else "engine_processing_failed"
        with transaction(engine, tenant) as session:
            task = valid_run(session, lease)
            if task:
                task.status, task.error_code, task.finished_at = "failed", code, datetime.now(UTC)
                session.add(
                    AuditEvent(
                        tenant_id=tenant,
                        actor_id=task.actor_id,
                        patient_id=task.patient_id,
                        action="analysis.failed",
                        resource_id=task.id,
                        # exception class only: messages can contain clinical text
                        details={"code": code, "exception": type(exc).__name__},
                    )
                )
