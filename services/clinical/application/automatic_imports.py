"""Route each input using its own documented identity, independently of the open chart."""

import hashlib
import json
from collections import defaultdict
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from clinical.application.imports import (
    IdempotencyConflict,
    NotFound,
    UploadedFile,
    enqueue_import,
    require_patient,
)
from clinical.application.ports import ObjectStore
from clinical.domain.evidence import InvalidSource, decode_source
from clinical.domain.patient_headers import PatientHeader, UnconfirmedIdentity, patient_header
from clinical.infrastructure.models import (
    AuditEvent,
    ImportBatch,
    ImportBatchItem,
    Patient,
    PatientAccess,
)


def enqueue_automatic_import(
    session: Session,
    store: ObjectStore,
    tenant: UUID,
    actor: UUID,
    key: str,
    files: tuple[UploadedFile, ...],
    max_file_bytes: int,
) -> ImportBatch:
    manifest = [(file.filename, hashlib.sha256(file.raw).hexdigest()) for file in files]
    digest = hashlib.sha256(json.dumps(manifest).encode()).hexdigest()
    lock = int.from_bytes(
        hashlib.sha256(f"auto-import:{tenant}:{actor}:{key}".encode()).digest()[:8], signed=True
    )
    session.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": lock})
    prior = session.scalar(
        select(ImportBatch).where(ImportBatch.actor_id == actor, ImportBatch.idempotency_key == key)
    )
    if prior:
        if prior.payload_hash != digest:
            raise IdempotencyConflict
        return prior

    headers: dict[int, PatientHeader] = {}
    errors: dict[int, str] = {}
    dates: dict[str, set[str]] = defaultdict(set)
    for index, file in enumerate(files):
        try:
            source = decode_source(file.raw, file.filename, max_file_bytes)
            if len(source.mrns) == 1:
                dates[next(iter(source.mrns))].update(source.birth_dates)
            headers[index] = patient_header(source)
        except (InvalidSource, UnconfirmedIdentity) as exc:
            errors[index] = str(exc)
    groups: dict[str, list[int]] = defaultdict(list)
    for index, header in headers.items():
        if len(dates[header.mrn]) > 1:
            errors[index] = "conflicting_identifiers"
        else:
            groups[header.mrn].append(index)

    batch = ImportBatch(tenant_id=tenant, actor_id=actor, idempotency_key=key, payload_hash=digest)
    session.add(batch)
    session.flush()
    assignments: dict[int, UUID] = {}
    # Consistent lock order avoids deadlocks for overlapping multi-patient batches.
    for mrn, indices in sorted(groups.items()):
        header = headers[indices[0]]
        identity_lock = int.from_bytes(
            hashlib.sha256(f"patient-identity:{tenant}:{mrn}".encode()).digest()[:8], signed=True
        )
        session.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": identity_lock})
        patient = session.scalar(select(Patient).where(Patient.mrn == mrn))
        if patient is not None:
            try:
                require_patient(session, patient.id, actor)
            except NotFound:
                errors.update({index: "identity_review_required" for index in indices})
                continue
            if patient.birth_date != header.birth_date:
                errors.update({index: "conflicting_identifiers" for index in indices})
                continue
        else:
            names = {headers[index].display_name for index in indices} - {mrn}
            patient = Patient(
                tenant_id=tenant,
                mrn=mrn,
                birth_date=header.birth_date,
                name=next(iter(names)) if len(names) == 1 else mrn,
            )
            session.add(patient)
            session.flush()
            session.add(PatientAccess(tenant_id=tenant, patient_id=patient.id, actor_id=actor))
            session.add(
                AuditEvent(
                    tenant_id=tenant,
                    actor_id=actor,
                    patient_id=patient.id,
                    action="patient.detected",
                    resource_id=batch.id,
                )
            )
            session.flush()
        job = enqueue_import(
            session,
            store,
            tenant,
            actor,
            patient.id,
            f"auto:{batch.id}:{hashlib.sha256(mrn.encode()).hexdigest()[:16]}",
            tuple(files[index] for index in indices),
        )
        assignments.update({index: job.id for index in indices})
    for index, file in enumerate(files):
        # Unassigned sources are retained for review, never attached to the currently open chart.
        sha256 = store.put(tenant, file.raw)
        session.add(
            ImportBatchItem(
                tenant_id=tenant,
                batch_id=batch.id,
                ordinal=index,
                filename=file.filename,
                sha256=sha256,
                job_id=assignments.get(index),
                error_code=errors.get(index),
            )
        )
    session.add(
        AuditEvent(
            tenant_id=tenant,
            actor_id=actor,
            patient_id=None,
            action="import_batch.accepted",
            resource_id=batch.id,
        )
    )
    session.flush()
    return batch
