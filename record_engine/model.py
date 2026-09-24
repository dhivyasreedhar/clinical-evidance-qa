"""Observations (what a document says), facts (what code decides) and the record."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Grounded(BaseModel):
    """One field value with the exact source text that states it."""

    name: str
    value: str
    quote: str
    block: str


class Recorded(BaseModel):
    """A record-time stamp (signature, entry, receipt...) — never an event time."""

    role: str
    value: str  # ISO date or datetime
    quote: str
    block: str


class Relation(BaseModel):
    type: Literal["corrects", "copy_of", "addendum", "none"] = "none"
    target_desc: str | None = None
    fields: list[str] = Field(default_factory=list)
    quote: str | None = None
    block: str | None = None


class Observation(BaseModel):
    id: str
    doc: str
    kind: str
    fields: list[Grounded]
    evidence_kind: str = "actual"
    attestation: str = "unknown"
    recorded: list[Recorded] = Field(default_factory=list)
    relation: Relation = Field(default_factory=Relation)
    source: Literal["extract", "sweep"] = "extract"

    def get(self, name: str) -> str | None:
        return next((f.value for f in self.fields if f.name == name and f.value != ""), None)

    def field(self, name: str) -> Grounded | None:
        return next((f for f in self.fields if f.name == name and f.value != ""), None)

    @property
    def blocks(self) -> list[str]:
        return sorted({f.block for f in self.fields})


Stance = Literal["supports", "contradicts", "superseded", "copy"]


class Evidence(BaseModel):
    observation: str
    block: str
    quote: str
    stance: Stance = "supports"
    value: Any = None


Status = Literal[
    "established", "corroborated", "documented", "conflicting", "superseded", "not_documented"
]


class Fact(BaseModel):
    id: str
    subject: str  # event id
    field: str
    value: Any = None
    scenarios: list[Any] = Field(default_factory=list)  # set when status == conflicting
    status: Status
    rule: str
    reason: str = ""
    valid_time: str | None = None  # when it happened (ISO date)
    recorded_time: str | None = None  # when it was recorded (latest supporting record time)
    evidence: list[Evidence] = Field(default_factory=list)

    def values(self) -> list[Any]:
        return self.scenarios if self.status == "conflicting" else [self.value]


class Event(BaseModel):
    id: str
    kind: str  # encounter | measurement | medication | goal | finding | charge | patient | document
    observations: list[str]
    keys: list[str] = Field(default_factory=list)
    link: dict[str, Any] = Field(default_factory=dict)  # how it was linked, with weights


class OpenItem(BaseModel):
    kind: Literal[
        "conflict",
        "candidate_link",
        "missing",
        "unextracted_mention",
        "invalid",
        "other_patient",
        "reading_disagreement",
    ]
    subject: str | None = None
    text: str
    blocks: list[str] = Field(default_factory=list)
    facts: list[str] = Field(default_factory=list)


class Record(BaseModel):
    version: str
    policy: str
    documents: list[dict[str, Any]]
    events: list[Event]
    facts: list[Fact]
    open_items: list[OpenItem]
    copies: dict[str, str] = Field(default_factory=dict)  # copy doc -> original doc

    def fact(self, fact_id: str) -> Fact | None:
        return next((f for f in self.facts if f.id == fact_id), None)

    def facts_of(self, subject: str) -> dict[str, Fact]:
        return {f.field: f for f in self.facts if f.subject == subject}
