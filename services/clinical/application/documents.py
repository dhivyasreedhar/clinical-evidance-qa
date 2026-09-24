"""Source document lifecycle: active set, snapshot publication, withdrawal and restoration.

Revisions are immutable and never deleted: withdrawing one appends an audited event and publishes a
new snapshot without it. Earlier snapshots, and record builds pinned to them, stay reproducible.
"""

import hashlib
import json
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from clinical.infrastructure.models import AuditEvent, DocumentStatusEvent, Revision, Snapshot


class DocumentStateError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def lock_patient(session: Session, tenant: UUID, patient_id: UUID) -> None:
    """Serialize source-set changes for one patient (imports, withdrawals, restorations)."""
    key = int.from_bytes(
        hashlib.sha256(f"patient:{tenant}:{patient_id}".encode()).digest()[:8], signed=True
    )
    session.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": key})


def withdrawn_ids(session: Session, patient_id: UUID) -> set[UUID]:
    """Revisions whose latest status event is a withdrawal."""
    latest: dict[UUID, str] = {}
    for event in session.scalars(
        select(DocumentStatusEvent)
        .where(DocumentStatusEvent.patient_id == patient_id)
        .order_by(DocumentStatusEvent.created_at, DocumentStatusEvent.id)
    ):
        latest[event.revision_id] = event.action
    return {rid for rid, action in latest.items() if action == "withdrawn"}


def publish_snapshot(session: Session, tenant: UUID, patient_id: UUID) -> Snapshot | None:
    """Publish a snapshot of the active revisions if it differs from the latest one."""
    withdrawn = withdrawn_ids(session, patient_id)
    revisions = [
        r
        for r in session.scalars(
            select(Revision).where(Revision.patient_id == patient_id).order_by(Revision.sha256)
        )
        if r.id not in withdrawn
    ]
    manifest = [{"revision_id": str(r.id), "sha256": r.sha256} for r in revisions]
    digest = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
    latest = session.scalar(
        select(Snapshot)
        .where(Snapshot.patient_id == patient_id)
        .order_by(Snapshot.sequence.desc())
        .limit(1)
    )
    if latest is not None and latest.manifest_hash == digest:
        return latest
    if latest is None and not revisions:
        return None
    snapshot = Snapshot(
        tenant_id=tenant,
        patient_id=patient_id,
        sequence=latest.sequence + 1 if latest else 1,
        manifest_hash=digest,
        manifest=manifest,
    )
    session.add(snapshot)
    session.flush()
    return snapshot


def set_document_status(
    session: Session,
    tenant: UUID,
    actor_id: UUID,
    patient_id: UUID,
    revision_id: UUID,
    action: str,
    reason: str | None = None,
) -> Snapshot | None:
    """Withdraw or restore one revision, audit it and publish the resulting snapshot."""
    lock_patient(session, tenant, patient_id)
    revision = session.scalar(
        select(Revision).where(Revision.id == revision_id, Revision.patient_id == patient_id)
    )
    if revision is None:
        raise DocumentStateError("document_not_found")
    withdrawn = revision.id in withdrawn_ids(session, patient_id)
    if (action == "withdrawn") == withdrawn:
        raise DocumentStateError(
            "document_already_withdrawn" if withdrawn else "document_not_withdrawn"
        )
    session.add(
        DocumentStatusEvent(
            tenant_id=tenant,
            patient_id=patient_id,
            revision_id=revision.id,
            actor_id=actor_id,
            action=action,
            reason=reason,
        )
    )
    session.flush()
    snapshot = publish_snapshot(session, tenant, patient_id)
    session.add(
        AuditEvent(
            tenant_id=tenant,
            actor_id=actor_id,
            patient_id=patient_id,
            resource_id=revision.id,
            action=f"document.{action}",
            details={
                "reason": reason,
                "snapshot_id": str(snapshot.id) if snapshot else None,
            },
        )
    )
    return snapshot
