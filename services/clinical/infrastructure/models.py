"""Persistence mappings. Tenant/patient composite foreign keys prevent scope drift."""

from datetime import date, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Scoped:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Patient(Scoped, Base):
    __tablename__ = "patients"
    name: Mapped[str] = mapped_column(String(200))
    mrn: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[date]
    archived: Mapped[bool] = mapped_column(default=False, server_default="false")
    __table_args__ = (
        UniqueConstraint("tenant_id", "id"),
        UniqueConstraint("tenant_id", "mrn"),
    )


class PatientAccess(Base):
    __tablename__ = "patient_access"
    tenant_id: Mapped[UUID] = mapped_column(primary_key=True)
    patient_id: Mapped[UUID] = mapped_column(primary_key=True)
    actor_id: Mapped[UUID] = mapped_column(primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(["tenant_id", "patient_id"], ["patients.tenant_id", "patients.id"]),
    )


class Job(Scoped, Base):
    __tablename__ = "jobs"
    patient_id: Mapped[UUID]
    actor_id: Mapped[UUID]
    idempotency_key: Mapped[str] = mapped_column(String(100))
    payload_hash: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(20), default="queued", index=True)
    attempt: Mapped[int] = mapped_column(Integer, default=0)
    lease_token: Mapped[UUID | None]
    lease_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_code: Mapped[str | None] = mapped_column(String(80))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        UniqueConstraint("tenant_id", "id"),
        UniqueConstraint("tenant_id", "patient_id", "id"),
        UniqueConstraint("tenant_id", "actor_id", "idempotency_key"),
        ForeignKeyConstraint(["tenant_id", "patient_id"], ["patients.tenant_id", "patients.id"]),
        CheckConstraint("status IN ('queued','running','succeeded','failed','canceled')"),
        CheckConstraint("attempt >= 0"),
    )


class Revision(Scoped, Base):
    __tablename__ = "document_revisions"
    patient_id: Mapped[UUID]
    sha256: Mapped[str] = mapped_column(String(64))
    filename: Mapped[str] = mapped_column(String(255))
    declared_id: Mapped[str | None] = mapped_column(String(255))
    line_count: Mapped[int]
    byte_count: Mapped[int]
    # This is exact decoded source text, NOT search normalization.
    text: Mapped[str] = mapped_column(Text)
    __table_args__ = (
        UniqueConstraint("tenant_id", "id"),
        UniqueConstraint("tenant_id", "patient_id", "id"),
        UniqueConstraint("tenant_id", "patient_id", "sha256"),
        ForeignKeyConstraint(["tenant_id", "patient_id"], ["patients.tenant_id", "patients.id"]),
        CheckConstraint("line_count > 0 AND byte_count > 0"),
    )


class Upload(Scoped, Base):
    __tablename__ = "uploads"
    patient_id: Mapped[UUID]
    job_id: Mapped[UUID]
    filename: Mapped[str] = mapped_column(String(255))
    sha256: Mapped[str] = mapped_column(String(64))
    byte_count: Mapped[int]
    status: Mapped[str] = mapped_column(String(20), default="pending")
    error_code: Mapped[str | None] = mapped_column(String(80))
    revision_id: Mapped[UUID | None]
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "patient_id", "job_id"], ["jobs.tenant_id", "jobs.patient_id", "jobs.id"]
        ),
        ForeignKeyConstraint(
            ["tenant_id", "patient_id", "revision_id"],
            [
                "document_revisions.tenant_id",
                "document_revisions.patient_id",
                "document_revisions.id",
            ],
        ),
        CheckConstraint("status IN ('pending','accepted','duplicate','quarantined','failed')"),
    )


class SourceSpan(Scoped, Base):
    __tablename__ = "source_spans"
    patient_id: Mapped[UUID]
    revision_id: Mapped[UUID]
    ordinal: Mapped[int]
    start_char: Mapped[int]
    end_char: Mapped[int]
    start_line: Mapped[int]
    end_line: Mapped[int]
    quote: Mapped[str] = mapped_column(Text)
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "patient_id", "revision_id"],
            [
                "document_revisions.tenant_id",
                "document_revisions.patient_id",
                "document_revisions.id",
            ],
        ),
        UniqueConstraint("tenant_id", "revision_id", "ordinal"),
        CheckConstraint(
            "start_char >= 0 AND end_char > start_char AND start_line > 0 AND end_line >= start_line"
        ),
    )


class Snapshot(Scoped, Base):
    __tablename__ = "snapshots"
    patient_id: Mapped[UUID]
    sequence: Mapped[int]
    manifest_hash: Mapped[str] = mapped_column(String(64))
    # UUID/hash-only manifest; clinical coverage is intentionally not claimed.
    manifest: Mapped[list[dict[str, str]]] = mapped_column(JSONB)
    __table_args__ = (
        UniqueConstraint("tenant_id", "patient_id", "id"),
        ForeignKeyConstraint(["tenant_id", "patient_id"], ["patients.tenant_id", "patients.id"]),
        UniqueConstraint("tenant_id", "patient_id", "sequence"),
    )


class DocumentStatusEvent(Scoped, Base):
    """Append-only withdraw/restore history; the latest event decides whether a revision is active."""

    __tablename__ = "document_status_events"
    patient_id: Mapped[UUID]
    revision_id: Mapped[UUID]
    actor_id: Mapped[UUID]
    action: Mapped[str] = mapped_column(String(20))
    reason: Mapped[str | None] = mapped_column(String(500))
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "patient_id", "revision_id"],
            [
                "document_revisions.tenant_id",
                "document_revisions.patient_id",
                "document_revisions.id",
            ],
        ),
        CheckConstraint("action IN ('withdrawn','restored')", name="document_status_action"),
    )


class AuditEvent(Scoped, Base):
    __tablename__ = "audit_events"
    actor_id: Mapped[UUID]
    patient_id: Mapped[UUID | None]
    action: Mapped[str] = mapped_column(String(60))
    resource_id: Mapped[UUID | None]
    details: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)


class ImportBatch(Scoped, Base):
    __tablename__ = "import_batches"
    actor_id: Mapped[UUID]
    idempotency_key: Mapped[str] = mapped_column(String(100))
    payload_hash: Mapped[str] = mapped_column(String(64))
    __table_args__ = (
        UniqueConstraint("tenant_id", "id"),
        UniqueConstraint("tenant_id", "actor_id", "idempotency_key"),
    )


class ImportBatchItem(Scoped, Base):
    __tablename__ = "import_batch_items"
    batch_id: Mapped[UUID]
    ordinal: Mapped[int]
    filename: Mapped[str] = mapped_column(String(255))
    sha256: Mapped[str] = mapped_column(String(64))
    job_id: Mapped[UUID | None]
    error_code: Mapped[str | None] = mapped_column(String(80))
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "batch_id"], ["import_batches.tenant_id", "import_batches.id"]
        ),
        ForeignKeyConstraint(["tenant_id", "job_id"], ["jobs.tenant_id", "jobs.id"]),
        UniqueConstraint("tenant_id", "batch_id", "ordinal"),
        CheckConstraint("(job_id IS NULL) != (error_code IS NULL)"),
    )


class AnalysisTask(Scoped, Base):
    __tablename__ = "analysis_tasks"
    patient_id: Mapped[UUID]
    actor_id: Mapped[UUID]
    snapshot_id: Mapped[UUID]
    abstraction_id: Mapped[UUID | None]
    kind: Mapped[str] = mapped_column(String(20))
    question: Mapped[str | None] = mapped_column(Text)
    model: Mapped[str] = mapped_column(String(100))
    prompt_version: Mapped[str] = mapped_column(String(50))
    schema_version: Mapped[str] = mapped_column(String(50))
    idempotency_key: Mapped[str] = mapped_column(String(100))
    payload_hash: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(20), default="queued", index=True)
    attempt: Mapped[int] = mapped_column(default=0)
    lease_token: Mapped[UUID | None]
    lease_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_code: Mapped[str | None] = mapped_column(String(80))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        UniqueConstraint("tenant_id", "patient_id", "id"),
        UniqueConstraint("tenant_id", "actor_id", "idempotency_key"),
        ForeignKeyConstraint(
            ["tenant_id", "patient_id", "snapshot_id"],
            ["snapshots.tenant_id", "snapshots.patient_id", "snapshots.id"],
        ),
        ForeignKeyConstraint(
            ["tenant_id", "patient_id", "abstraction_id"],
            ["analysis_tasks.tenant_id", "analysis_tasks.patient_id", "analysis_tasks.id"],
        ),
        CheckConstraint("kind IN ('engine_record','engine_answer')", name="analysis_kind"),
        CheckConstraint("status IN ('queued','running','succeeded','failed')"),
        CheckConstraint("attempt >= 0"),
        CheckConstraint(
            "(kind IN ('engine_record') AND abstraction_id IS NULL AND question IS NULL) OR "
            "(kind IN ('engine_answer') AND abstraction_id IS NOT NULL AND question IS NOT NULL)",
            name="analysis_kind_payload",
        ),
    )


class AnalysisResult(Scoped, Base):
    __tablename__ = "analysis_results"
    patient_id: Mapped[UUID]
    task_id: Mapped[UUID]
    data: Mapped[dict[str, Any]] = mapped_column(JSONB)
    usage: Mapped[dict[str, Any]] = mapped_column(JSONB)
    __table_args__ = (
        UniqueConstraint("tenant_id", "task_id"),
        ForeignKeyConstraint(
            ["tenant_id", "patient_id", "task_id"],
            ["analysis_tasks.tenant_id", "analysis_tasks.patient_id", "analysis_tasks.id"],
        ),
    )
