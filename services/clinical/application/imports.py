import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import Engine, or_, select, text
from sqlalchemy.orm import Session

from clinical.application.documents import (
    lock_patient,
    publish_snapshot,
    set_document_status,
    withdrawn_ids,
)
from clinical.application.ports import ObjectStore
from clinical.domain.evidence import InvalidSource, decode_source, identity_disposition
from clinical.infrastructure.database import transaction
from clinical.infrastructure.models import (
    AuditEvent,
    Job,
    Patient,
    PatientAccess,
    Revision,
    SourceSpan,
    Upload,
)


class NotFound(Exception):
    pass


class IdempotencyConflict(Exception):
    pass


def require_patient(session: Session, patient_id: UUID, actor_id: UUID) -> Patient:
    patient = session.scalar(
        select(Patient)
        .join(
            PatientAccess,
            (PatientAccess.patient_id == Patient.id)
            & (PatientAccess.tenant_id == Patient.tenant_id),
        )
        .where(
            Patient.id == patient_id,
            PatientAccess.actor_id == actor_id,
            Patient.archived.is_(False),
        )
    )
    if patient is None:
        raise NotFound
    return patient


@dataclass(frozen=True)
class UploadedFile:
    filename: str
    raw: bytes


def enqueue_import(
    session: Session,
    store: ObjectStore,
    tenant: UUID,
    actor: UUID,
    patient_id: UUID,
    key: str,
    files: tuple[UploadedFile, ...],
) -> Job:
    require_patient(session, patient_id, actor)
    manifest = [(f.filename, hashlib.sha256(f.raw).hexdigest()) for f in files]
    payload_hash = hashlib.sha256(json.dumps([str(patient_id), manifest]).encode()).hexdigest()
    # Serialize idempotency-key contenders before any database or object mutation.

    lock_key = int.from_bytes(
        hashlib.sha256(f"{tenant}:{actor}:{key}".encode()).digest()[:8], signed=True
    )
    session.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": lock_key})
    prior = session.scalar(select(Job).where(Job.actor_id == actor, Job.idempotency_key == key))
    if prior:
        if prior.payload_hash != payload_hash:
            raise IdempotencyConflict
        return prior
    job = Job(
        tenant_id=tenant,
        actor_id=actor,
        patient_id=patient_id,
        idempotency_key=key,
        payload_hash=payload_hash,
    )
    session.add(job)
    session.flush()
    for file in files:
        digest = store.put(tenant, file.raw)
        session.add(
            Upload(
                tenant_id=tenant,
                patient_id=patient_id,
                job_id=job.id,
                filename=file.filename,
                sha256=digest,
                byte_count=len(file.raw),
            )
        )
    session.add(
        AuditEvent(
            tenant_id=tenant,
            actor_id=actor,
            patient_id=patient_id,
            action="import.accepted",
            resource_id=job.id,
        )
    )
    return job


@dataclass(frozen=True)
class Lease:
    job_id: UUID
    token: UUID


def claim_job(engine: Engine, tenant: UUID) -> Lease | None:
    with transaction(engine, tenant) as session:
        now = datetime.now(UTC)
        job = session.scalar(
            select(Job)
            .where(
                or_(
                    Job.status == "queued",
                    (Job.status == "running") & (Job.lease_until < now),
                )
            )
            .order_by(Job.created_at, Job.id)
            .with_for_update(skip_locked=True)
            .limit(1)
        )
        if not job:
            return None
        if job.attempt >= 3:
            job.status, job.error_code, job.finished_at = "failed", "attempts_exhausted", now
            return None
        job.status = "running"
        job.attempt += 1
        job.lease_token = uuid4()
        job.lease_until = now + timedelta(seconds=60)
        return Lease(job.id, job.lease_token)


def process_job(
    engine: Engine,
    store: ObjectStore,
    tenant: UUID,
    lease: Lease,
    max_file_bytes: int,
) -> bool:
    """Short source-only stage is atomic. Crash rolls back; expired leases are reclaimable.

    No external service calls are made inside this transaction; model calls run in
    engine_runs.py, outside transactions, with renewed leases and fenced publication.
    """
    with transaction(engine, tenant) as session:
        job = session.scalar(select(Job).where(Job.id == lease.job_id).with_for_update())
        if (
            not job
            or job.status != "running"
            or job.lease_token != lease.token
            or job.lease_until is None
            or job.lease_until < datetime.now(UTC)
        ):
            return False
        try:
            patient = require_patient(session, job.patient_id, job.actor_id)
        except NotFound:
            job.status, job.error_code, job.finished_at = (
                "failed",
                "access_revoked",
                datetime.now(UTC),
            )
            return False
        # Serialize concurrent imports for this patient. The snapshot includes the
        # latest committed manifest, so simultaneous imports cannot lose evidence.
        lock_patient(session, tenant, patient.id)
        uploads = session.scalars(
            select(Upload).where(Upload.job_id == job.id).order_by(Upload.created_at, Upload.id)
        ).all()
        for upload in uploads:
            try:
                raw = store.get(tenant, upload.sha256)
                source = decode_source(raw, upload.filename, max_file_bytes)
            except (InvalidSource, ValueError, OSError):
                upload.status, upload.error_code = "failed", "source_validation_failed"
                continue
            issue = identity_disposition(source, patient.mrn, patient.birth_date.isoformat())
            if issue:
                upload.status, upload.error_code = "quarantined", issue
                continue
            existing = session.scalar(
                select(Revision).where(
                    Revision.patient_id == patient.id,
                    Revision.sha256 == source.sha256,
                )
            )
            if existing:
                upload.status, upload.revision_id = "duplicate", existing.id
                if existing.id in withdrawn_ids(session, patient.id):
                    # Re-uploading a withdrawn document restores it.
                    set_document_status(
                        session,
                        tenant,
                        job.actor_id,
                        patient.id,
                        existing.id,
                        "restored",
                        "re-uploaded",
                    )
                continue
            revision = Revision(
                tenant_id=tenant,
                patient_id=patient.id,
                sha256=source.sha256,
                filename=upload.filename,
                declared_id=source.declared_id,
                line_count=source.line_count,
                byte_count=len(raw),
                text=source.text,
            )
            session.add(revision)
            session.flush()
            for ordinal, span in enumerate(source.blocks):
                span.validate(source.text)
                session.add(
                    SourceSpan(
                        tenant_id=tenant,
                        patient_id=patient.id,
                        revision_id=revision.id,
                        ordinal=ordinal,
                        start_char=span.start_char,
                        end_char=span.end_char,
                        start_line=span.start_line,
                        end_line=span.end_line,
                        quote=span.quote,
                    )
                )
            upload.status, upload.revision_id = "accepted", revision.id
        session.flush()
        publish_snapshot(session, tenant, patient.id)
        job.status = "succeeded"
        job.finished_at = datetime.now(UTC)
        job.lease_until = None
        session.add(
            AuditEvent(
                tenant_id=tenant,
                actor_id=job.actor_id,
                patient_id=patient.id,
                resource_id=job.id,
                action="import.processed",
            )
        )
        return True
