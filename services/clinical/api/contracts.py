from datetime import date, datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


class PatientCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=200)
    mrn: str = Field(min_length=1, max_length=100, pattern=r"^[A-Za-z0-9_-]+$")
    birth_date: date


class PatientOut(PatientCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class SessionOut(BaseModel):
    actor_id: UUID
    csrf_token: str
    mode: Literal["synthetic_development"] = "synthetic_development"


class UploadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    filename: str
    status: str
    error_code: str | None
    revision_id: UUID | None


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    patient_id: UUID
    status: str
    attempt: int
    error_code: str | None
    created_at: datetime
    uploads: list[UploadOut]


class ImportIssueOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    filename: str
    error_code: str


class ImportBatchOut(BaseModel):
    id: UUID
    jobs: list[JobOut]
    issues: list[ImportIssueOut]


class RevisionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    filename: str
    declared_id: str | None
    sha256: str
    line_count: int
    byte_count: int
    created_at: datetime
    withdrawn: bool = False


class DocumentWithdraw(BaseModel):
    reason: str = Field(min_length=1, max_length=500)


class DocumentStatusOut(BaseModel):
    revision_id: UUID
    withdrawn: bool
    snapshot_id: UUID | None


class SpanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    start_char: int
    end_char: int
    start_line: int
    end_line: int
    quote: str


class SourceOut(RevisionOut):
    text: str
    spans: list[SpanOut]
    segmentation: Literal["structural_v1"] = "structural_v1"


class SnapshotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    sequence: int
    manifest_hash: str
    created_at: datetime
    manifest: list[dict[str, str]]


class CitationOut(BaseModel):
    span_id: str
    revision_id: str
    filename: str
    start_line: int
    end_line: int
    quote: str


class ModelStatusOut(BaseModel):
    provider: Literal["anthropic"] = "anthropic"
    configured: bool
    model: str
    # the engine version a record must have been built with to be answered over
    engine_version: str


class RecordCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    snapshot_id: UUID


class QuestionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    record_id: UUID
    question: str = Field(min_length=1, max_length=2000)


class RunUsageOut(BaseModel):
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    calls: int
    cached_calls: int


class RunOut(BaseModel):
    id: UUID
    kind: Literal["engine_record", "engine_answer"]
    snapshot_id: UUID
    record_id: UUID | None
    question: str | None
    status: str
    error_code: str | None
    model: str
    prompt_version: str
    schema_version: str
    created_at: datetime
    usage: RunUsageOut | None = None


class RunVersionOut(BaseModel):
    version: str


def _text(value: Any) -> Any:
    """A record value shown as text: several values (for example two documented reasons, or a
    value with conflicting sources) are joined rather than rejected."""
    if isinstance(value, dict) and "scenarios" in value:
        return " or ".join(str(v) for v in value["scenarios"]) or None
    if isinstance(value, list):
        return "; ".join(str(v) for v in value) or None
    return None if value is None else str(value)


def _numbers(value: Any) -> Any:
    """A measured quantity as its possible values: one number, or one per scenario."""
    if isinstance(value, dict) and "scenarios" in value:
        value = value["scenarios"]
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


Text = Annotated[str | None, BeforeValidator(_text)]
Numbers = Annotated[list[float], BeforeValidator(_numbers)]


# The record view is computed by code from the reconciled record; nothing in it is model prose
# except quoted finding text. Values with conflicting sources carry every scenario.


class LedgerRow(BaseModel):
    id: str
    date: Text
    weekday: Text
    service: Text
    attendance: Text
    disposition: Text
    minutes: Numbers
    status: Text
    reason: Text
    citations: list[CitationOut]


class GoalThreshold(BaseModel):
    threshold: str
    measured: Numbers
    outcome: str


class WeekRow(BaseModel):
    week: str
    partial: bool
    sessions: int | None
    days: int | None
    minutes: Numbers
    goal: Text = None
    thresholds: list[GoalThreshold] = Field(default_factory=list)


class FactOut(BaseModel):
    field: str
    values: list[Any]
    status: str
    reason: str
    citations: list[CitationOut]


class EventOut(BaseModel):
    id: str
    kind: str
    facts: list[FactOut]


class FindingOut(BaseModel):
    id: str
    date: Text
    type: Text
    reporter: Text
    text: Any
    status: str
    citations: list[CitationOut]


class RecordDocumentOut(BaseModel):
    key: str
    revision_id: str | None
    filename: str
    title: Text
    issuer: Text
    copy_of: Text
    set_aside: Text
    service_dates: list[str]


class OpenItemOut(BaseModel):
    kind: str
    subject: Text
    text: str
    citations: list[CitationOut]


class RecordView(BaseModel):
    events_total: int
    facts_total: int
    encounters: list[LedgerRow]
    weeks: list[WeekRow]
    totals: WeekRow | None
    events: list[EventOut]
    findings: list[FindingOut]
    documents: list[RecordDocumentOut]
    open_items: list[OpenItemOut]


class StatementOut(BaseModel):
    text: str
    kind: str
    citations: list[CitationOut]


class AnswerOut(BaseModel):
    status: str
    statements: list[StatementOut]
    # checked statements the question did not ask about, held back from the answer
    omitted: list[StatementOut] = Field(default_factory=list)
    reasons: list[str]


class RunDetail(RunOut):
    record: RecordView | None = None
    answer: AnswerOut | None = None
