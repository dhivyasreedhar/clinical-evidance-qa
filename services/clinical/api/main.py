import hashlib
import json
import secrets
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator, Sequence
from contextlib import asynccontextmanager
from pathlib import PurePosixPath
from typing import Annotated, Literal
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.datastructures import UploadFile

from clinical.api.auth import COOKIE, Principal, principal, serializer, verify_origin
from clinical.api.contracts import (
    DocumentStatusOut,
    DocumentWithdraw,
    ImportBatchOut,
    ImportIssueOut,
    JobOut,
    ModelStatusOut,
    PatientCreate,
    PatientOut,
    QuestionCreate,
    RecordCreate,
    RevisionOut,
    RunDetail,
    RunOut,
    RunUsageOut,
    RunVersionOut,
    SessionOut,
    SnapshotOut,
    SourceOut,
    SpanOut,
    UploadOut,
)
from clinical.application.automatic_imports import enqueue_automatic_import
from clinical.application.documents import (
    DocumentStateError,
    set_document_status,
    withdrawn_ids,
)
from clinical.application.engine_runs import KINDS, RunError, enqueue_run, versions
from clinical.application.imports import (
    IdempotencyConflict,
    NotFound,
    UploadedFile,
    enqueue_import,
    require_patient,
)
from clinical.infrastructure.config import Settings
from clinical.infrastructure.database import make_engine, transaction
from clinical.infrastructure.models import (
    AnalysisResult,
    AnalysisTask,
    AuditEvent,
    ImportBatch,
    ImportBatchItem,
    Job,
    Patient,
    PatientAccess,
    Revision,
    Snapshot,
    SourceSpan,
    Upload,
)
from clinical.infrastructure.objects import LocalObjectStore
from record_engine import llm

Auth = Annotated[Principal, Depends(principal)]


def database(request: Request, auth: Auth) -> Iterator[Session]:
    with transaction(request.app.state.engine, auth.tenant_id) as session:
        yield session


DB = Annotated[Session, Depends(database, scope="function")]


def run_out(task: AnalysisTask, result: AnalysisResult | None) -> RunOut:
    return RunOut(
        id=task.id,
        kind=task.kind,
        snapshot_id=task.snapshot_id,
        record_id=task.abstraction_id,
        question=task.question,
        status=task.status,
        error_code=task.error_code,
        model=task.model,
        prompt_version=task.prompt_version,
        schema_version=task.schema_version,
        created_at=task.created_at,
        usage=RunUsageOut.model_validate(result.usage) if result else None,
    )


def job_response(session: Session, job: Job) -> JobOut:
    uploads = session.scalars(
        select(Upload).where(Upload.job_id == job.id).order_by(Upload.filename, Upload.id)
    ).all()
    return JobOut(
        id=job.id,
        patient_id=job.patient_id,
        status=job.status,
        attempt=job.attempt,
        error_code=job.error_code,
        created_at=job.created_at,
        uploads=[UploadOut.model_validate(u) for u in uploads],
    )


def batch_response(session: Session, batch: ImportBatch, actor: UUID) -> ImportBatchOut:
    items = session.scalars(
        select(ImportBatchItem)
        .where(ImportBatchItem.batch_id == batch.id)
        .order_by(ImportBatchItem.ordinal)
    ).all()
    jobs = session.scalars(
        select(Job)
        .join(Patient, (Patient.id == Job.patient_id) & (Patient.tenant_id == Job.tenant_id))
        .join(
            PatientAccess,
            (PatientAccess.patient_id == Patient.id)
            & (PatientAccess.tenant_id == Patient.tenant_id),
        )
        .where(Patient.archived.is_(False), PatientAccess.actor_id == actor)
        .where(Job.id.in_({item.job_id for item in items if item.job_id}))
        .order_by(Job.created_at, Job.id)
    ).all()
    return ImportBatchOut(
        id=batch.id,
        jobs=[job_response(session, job) for job in jobs],
        issues=[ImportIssueOut.model_validate(item) for item in items if item.error_code],
    )


async def read_uploads(request: Request, settings: Settings) -> tuple[UploadedFile, ...]:
    files: list[UploadedFile] = []
    size = 0
    async with request.form(max_files=settings.max_files, max_fields=0) as form:
        for value in form.getlist("files"):
            if not isinstance(value, UploadFile):
                raise HTTPException(422, detail="files_required")
            raw = await value.read(settings.max_file_bytes + 1)
            size += len(raw)
            if len(raw) > settings.max_file_bytes or size > settings.max_import_bytes:
                raise HTTPException(413, detail="import_size_limit")
            filename = PurePosixPath((value.filename or "untitled").replace("\\", "/")).name
            if len(filename) > 255:
                raise HTTPException(422, detail="filename_too_long")
            files.append(UploadedFile(filename, raw))
    if not files:
        raise HTTPException(422, detail="files_required")
    return tuple(files)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    engine = make_engine(settings.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        yield
        engine.dispose()

    app = FastAPI(title="Clinical Evidence API", version="0.1.0", lifespan=lifespan)
    app.state.settings, app.state.engine = settings, engine
    app.state.store = LocalObjectStore(settings.object_root)

    @app.middleware("http")
    async def request_metadata(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = str(uuid4())
        request.state.request_id = request_id
        if request.url.path.endswith("/imports") and request.method == "POST":
            try:
                length = int(request.headers.get("content-length", "0"))
            except ValueError:
                length = 0
            if length <= 0 or length > settings.max_import_bytes + 1024 * 1024:
                return JSONResponse(
                    status_code=413,
                    content={"detail": "import_size_limit", "request_id": request_id},
                )
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.exception_handler(NotFound)
    async def not_found(request: Request, exc: NotFound) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": "not_found"})

    @app.exception_handler(RunError)
    async def run_error(request: Request, exc: RunError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": exc.code})

    @app.exception_handler(DocumentStateError)
    async def document_state_error(request: Request, exc: DocumentStateError) -> JSONResponse:
        status = 404 if exc.code == "document_not_found" else 409
        return JSONResponse(status_code=status, content={"detail": exc.code})

    @app.exception_handler(IdempotencyConflict)
    async def idempotency_conflict(request: Request, exc: IdempotencyConflict) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": "idempotency_key_reused"})

    @app.exception_handler(IntegrityError)
    async def integrity_error(request: Request, exc: IntegrityError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": "conflicting_record"})

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        # Never expose SQL bound parameters (which can contain source text).
        return JSONResponse(status_code=503, content={"detail": "database_unavailable"})

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "detail": "invalid_input",
                "fields": [".".join(str(x) for x in e["loc"]) for e in exc.errors()],
            },
        )

    @app.get("/api/v1/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "synthetic_development", "engine": versions()[0]}

    @app.get("/api/v1/ready")
    def ready() -> dict[str, str]:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ready"}

    @app.post("/api/v1/dev-session", response_model=SessionOut)
    def sign_in(request: Request, response: Response) -> SessionOut:
        verify_origin(request)
        csrf = secrets.token_urlsafe(32)
        token = serializer(settings).dumps(
            {"tenant": str(settings.dev_tenant), "actor": str(settings.dev_actor), "csrf": csrf}
        )
        response.set_cookie(
            COOKIE, token, max_age=8 * 3600, httponly=True, samesite="strict", secure=False
        )
        return SessionOut(actor_id=settings.dev_actor, csrf_token=csrf)

    @app.get("/api/v1/session", response_model=SessionOut)
    def get_session(auth: Auth) -> SessionOut:
        return SessionOut(actor_id=auth.actor_id, csrf_token=auth.csrf)

    @app.delete("/api/v1/session", status_code=204)
    def sign_out(auth: Auth, response: Response) -> None:
        response.delete_cookie(COOKIE)

    @app.post("/api/v1/patients", response_model=PatientOut, status_code=201)
    def create_patient(payload: PatientCreate, auth: Auth, db: DB) -> Patient:
        patient = Patient(tenant_id=auth.tenant_id, **payload.model_dump())
        db.add(patient)
        db.flush()
        db.add(
            PatientAccess(tenant_id=auth.tenant_id, patient_id=patient.id, actor_id=auth.actor_id)
        )
        db.add(
            AuditEvent(
                tenant_id=auth.tenant_id,
                actor_id=auth.actor_id,
                patient_id=patient.id,
                action="patient.created",
                resource_id=patient.id,
            )
        )
        return patient

    @app.get("/api/v1/patients", response_model=list[PatientOut])
    def patients(
        auth: Auth, db: DB, after: UUID | None = None, limit: int = Query(100, ge=1, le=100)
    ) -> Sequence[Patient]:
        query = (
            select(Patient)
            .join(
                PatientAccess,
                (PatientAccess.patient_id == Patient.id)
                & (PatientAccess.tenant_id == Patient.tenant_id),
            )
            .where(PatientAccess.actor_id == auth.actor_id, Patient.archived.is_(False))
        )
        if after:
            query = query.where(Patient.id > after)
        return db.scalars(query.order_by(Patient.id).limit(limit)).all()

    @app.post("/api/v1/imports", response_model=ImportBatchOut, status_code=202)
    async def automatic_import(
        request: Request,
        auth: Auth,
        db: DB,
        idempotency_key: Annotated[str, Header(min_length=1, max_length=100)],
    ) -> ImportBatchOut:
        files = await read_uploads(request, settings)
        batch = enqueue_automatic_import(
            db,
            app.state.store,
            auth.tenant_id,
            auth.actor_id,
            idempotency_key,
            files,
            settings.max_file_bytes,
        )
        return batch_response(db, batch, auth.actor_id)

    @app.get("/api/v1/imports", response_model=list[ImportBatchOut])
    def import_batches(auth: Auth, db: DB, after: UUID | None = None) -> list[ImportBatchOut]:
        query = select(ImportBatch).where(ImportBatch.actor_id == auth.actor_id)
        if after:
            query = query.where(ImportBatch.id > after)
        return [
            batch_response(db, batch, auth.actor_id)
            for batch in db.scalars(query.order_by(ImportBatch.id).limit(100))
        ]

    @app.post("/api/v1/patients/{patient_id}/imports", response_model=JobOut, status_code=202)
    async def import_sources(
        patient_id: UUID,
        request: Request,
        auth: Auth,
        db: DB,
        idempotency_key: Annotated[str, Header(min_length=1, max_length=100)],
    ) -> JobOut:
        require_patient(db, patient_id, auth.actor_id)
        files = await read_uploads(request, settings)
        job = enqueue_import(
            db,
            app.state.store,
            auth.tenant_id,
            auth.actor_id,
            patient_id,
            idempotency_key,
            tuple(files),
        )
        db.flush()
        return job_response(db, job)

    @app.get("/api/v1/jobs/{job_id}", response_model=JobOut)
    def get_job(job_id: UUID, auth: Auth, db: DB) -> JobOut:
        job = db.get(Job, job_id)
        if not job:
            raise NotFound
        require_patient(db, job.patient_id, auth.actor_id)
        return job_response(db, job)

    @app.get("/api/v1/patients/{patient_id}/jobs", response_model=list[JobOut])
    def jobs(patient_id: UUID, auth: Auth, db: DB, after: UUID | None = None) -> list[JobOut]:
        require_patient(db, patient_id, auth.actor_id)
        query = select(Job).where(Job.patient_id == patient_id)
        if after:
            query = query.where(Job.id > after)
        return [job_response(db, job) for job in db.scalars(query.order_by(Job.id).limit(100))]

    @app.get("/api/v1/patients/{patient_id}/documents", response_model=list[RevisionOut])
    def documents(
        patient_id: UUID, auth: Auth, db: DB, after: UUID | None = None
    ) -> list[RevisionOut]:
        require_patient(db, patient_id, auth.actor_id)
        query = select(Revision).where(Revision.patient_id == patient_id)
        if after:
            query = query.where(Revision.id > after)
        withdrawn = withdrawn_ids(db, patient_id)
        return [
            RevisionOut.model_validate(r).model_copy(update={"withdrawn": r.id in withdrawn})
            for r in db.scalars(query.order_by(Revision.id).limit(100))
        ]

    def change_document(
        patient_id: UUID,
        revision_id: UUID,
        auth: Principal,
        db: Session,
        action: str,
        reason: str | None,
    ) -> DocumentStatusOut:
        require_patient(db, patient_id, auth.actor_id)
        snapshot = set_document_status(
            db, auth.tenant_id, auth.actor_id, patient_id, revision_id, action, reason
        )
        return DocumentStatusOut(
            revision_id=revision_id,
            withdrawn=action == "withdrawn",
            snapshot_id=snapshot.id if snapshot else None,
        )

    @app.post(
        "/api/v1/patients/{patient_id}/documents/{revision_id}/withdraw",
        response_model=DocumentStatusOut,
    )
    def withdraw_document(
        patient_id: UUID, revision_id: UUID, payload: DocumentWithdraw, auth: Auth, db: DB
    ) -> DocumentStatusOut:
        """Remove a document from the case. The source stays preserved for audit; a new snapshot
        without it is published, and its record is rebuilt automatically when a Claude key is
        configured."""
        return change_document(patient_id, revision_id, auth, db, "withdrawn", payload.reason)

    @app.post(
        "/api/v1/patients/{patient_id}/documents/{revision_id}/restore",
        response_model=DocumentStatusOut,
    )
    def restore_document(
        patient_id: UUID, revision_id: UUID, auth: Auth, db: DB
    ) -> DocumentStatusOut:
        return change_document(patient_id, revision_id, auth, db, "restored", None)

    @app.get("/api/v1/patients/{patient_id}/snapshots", response_model=list[SnapshotOut])
    def snapshots(
        patient_id: UUID, auth: Auth, db: DB, before: int | None = None
    ) -> Sequence[Snapshot]:
        require_patient(db, patient_id, auth.actor_id)
        query = select(Snapshot).where(Snapshot.patient_id == patient_id)
        if before:
            query = query.where(Snapshot.sequence < before)
        return db.scalars(query.order_by(Snapshot.sequence.desc()).limit(100)).all()

    @app.get("/api/v1/source-revisions/{revision_id}", response_model=SourceOut)
    def source(revision_id: UUID, auth: Auth, db: DB) -> SourceOut:
        revision = db.get(Revision, revision_id)
        if not revision:
            raise NotFound
        require_patient(db, revision.patient_id, auth.actor_id)
        db.add(
            AuditEvent(
                tenant_id=auth.tenant_id,
                actor_id=auth.actor_id,
                patient_id=revision.patient_id,
                action="source.read",
                resource_id=revision.id,
            )
        )
        spans = db.scalars(
            select(SourceSpan)
            .where(SourceSpan.revision_id == revision.id)
            .order_by(SourceSpan.ordinal)
        ).all()
        return SourceOut(
            **RevisionOut.model_validate(revision).model_dump(),
            text=revision.text,
            spans=[SpanOut.model_validate(span) for span in spans],
        )

    @app.get("/api/v1/source-revisions/{revision_id}/spans/{span_id}", response_model=SpanOut)
    def citation(revision_id: UUID, span_id: UUID, auth: Auth, db: DB) -> SourceSpan:
        span = db.get(SourceSpan, span_id)
        if not span or span.revision_id != revision_id:
            raise NotFound
        require_patient(db, span.patient_id, auth.actor_id)
        db.add(
            AuditEvent(
                tenant_id=auth.tenant_id,
                actor_id=auth.actor_id,
                patient_id=span.patient_id,
                action="citation.read",
                resource_id=span.id,
            )
        )
        return span

    @app.get("/api/v1/model-status", response_model=ModelStatusOut)
    def model_status(auth: Auth) -> ModelStatusOut:
        return ModelStatusOut(
            configured=bool(settings.anthropic_api_key.get_secret_value()),
            model=llm.WRITER,
            engine_version=versions()[0],
        )

    def patient_run(db: Session, patient_id: UUID, run_id: UUID) -> AnalysisTask:
        task = db.scalar(
            select(AnalysisTask).where(
                AnalysisTask.id == run_id,
                AnalysisTask.patient_id == patient_id,
                AnalysisTask.kind.in_(KINDS),
            )
        )
        if task is None:
            raise NotFound()
        return task

    @app.post("/api/v1/patients/{patient_id}/records", response_model=RunOut, status_code=202)
    def start_record(
        patient_id: UUID,
        payload: RecordCreate,
        auth: Auth,
        db: DB,
        idempotency_key: Annotated[str, Header(min_length=1, max_length=100)],
    ) -> RunOut:
        """Queue a record build: extraction, linking and reconciliation of the snapshot's
        documents."""
        task = enqueue_run(
            db,
            settings,
            auth.tenant_id,
            auth.actor_id,
            patient_id,
            idempotency_key,
            snapshot_id=payload.snapshot_id,
        )
        return run_out(task, None)

    @app.post("/api/v1/patients/{patient_id}/answers", response_model=RunOut, status_code=202)
    def start_answer(
        patient_id: UUID,
        payload: QuestionCreate,
        auth: Auth,
        db: DB,
        idempotency_key: Annotated[str, Header(min_length=1, max_length=100)],
    ) -> RunOut:
        """Queue a question over a finished record build."""
        task = enqueue_run(
            db,
            settings,
            auth.tenant_id,
            auth.actor_id,
            patient_id,
            idempotency_key,
            record_id=payload.record_id,
            question=payload.question,
        )
        return run_out(task, None)

    @app.get("/api/v1/patients/{patient_id}/runs", response_model=list[RunOut])
    def runs(patient_id: UUID, auth: Auth, db: DB) -> list[RunOut]:
        """Record builds and questions, newest first."""
        require_patient(db, patient_id, auth.actor_id)
        tasks = list(
            db.scalars(
                select(AnalysisTask)
                .where(AnalysisTask.patient_id == patient_id, AnalysisTask.kind.in_(KINDS))
                .order_by(AnalysisTask.created_at.desc(), AnalysisTask.id)
                .limit(200)
            )
        )
        usage = {
            task_id: value
            for task_id, value in db.execute(
                select(AnalysisResult.task_id, AnalysisResult.usage).where(
                    AnalysisResult.task_id.in_([t.id for t in tasks])
                )
            ).tuples()
        }
        return [
            run_out(task, AnalysisResult(usage=usage[task.id]) if task.id in usage else None)
            for task in tasks
        ]

    @app.get("/api/v1/patients/{patient_id}/runs/version", response_model=RunVersionOut)
    def runs_version(patient_id: UUID, auth: Auth, db: DB) -> RunVersionOut:
        """Cheap change marker so clients poll this instead of re-downloading every run."""
        require_patient(db, patient_id, auth.actor_id)
        rows = db.execute(
            select(
                AnalysisTask.id,
                AnalysisTask.status,
                AnalysisTask.error_code,
                AnalysisTask.finished_at,
            )
            .where(AnalysisTask.patient_id == patient_id)
            .order_by(AnalysisTask.id)
        ).all()
        marker = json.dumps([[str(v) for v in row] for row in rows])
        return RunVersionOut(version=hashlib.sha256(marker.encode()).hexdigest()[:32])

    @app.get("/api/v1/patients/{patient_id}/runs/{run_id}", response_model=RunDetail)
    def run_detail(patient_id: UUID, run_id: UUID, auth: Auth, db: DB) -> RunDetail:
        """One run with its result: the record view for a record build, the cited answer for a
        question."""
        require_patient(db, patient_id, auth.actor_id)
        task = patient_run(db, patient_id, run_id)
        result = db.scalar(select(AnalysisResult).where(AnalysisResult.task_id == task.id))
        data = result.data if result else {}
        return RunDetail(
            **run_out(task, result).model_dump(),
            record=data.get("view"),
            answer=data.get("answer"),
        )

    @app.get("/api/v1/patients/{patient_id}/records/{run_id}/export")
    def export_record(
        patient_id: UUID,
        run_id: UUID,
        auth: Auth,
        db: DB,
        format: Annotated[Literal["json", "markdown"], Query()] = "json",
    ) -> Response:
        """The full reconciled record (every fact with its rule and quoted evidence) as JSON, or
        the readable abstraction as Markdown, as a file download."""
        require_patient(db, patient_id, auth.actor_id)
        task = patient_run(db, patient_id, run_id)
        result = db.scalar(select(AnalysisResult).where(AnalysisResult.task_id == task.id))
        if task.kind != "engine_record" or result is None:
            raise NotFound()
        db.add(
            AuditEvent(
                tenant_id=auth.tenant_id,
                actor_id=auth.actor_id,
                patient_id=patient_id,
                action="record.exported",
                resource_id=task.id,
                details={"format": format},
            )
        )
        if format == "markdown":
            body, media, name = result.data["abstraction_markdown"], "text/markdown", "md"
        else:
            body, media, name = (
                json.dumps(result.data["record"], indent=1),
                "application/json",
                "json",
            )
        return Response(
            body,
            media_type=media,
            headers={"Content-Disposition": f'attachment; filename="record-{run_id}.{name}"'},
        )

    return app
