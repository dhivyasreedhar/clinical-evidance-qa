# Record engine: observations first, facts by code

## Status

Accepted, 24 Sep 2026.

## Context

Clinical questions about an episode of care depend on how records relate: corrections, copies,
competing accounts of the same visit, entries for another patient, and counting rules that come
from the care plan. A model that reads documents and writes conclusions can resolve these silently
or add numbers itself, and its conclusions are hard to check.

## Decision

- **Extraction records observations, not conclusions.** One model call per document returns
  observations whose every field is `{value, quote, block}`. Code rejects a value its own quote
  does not contain and sweeps the text for times, dates, durations, IDs and scores no quote
  covers; uncovered mentions get one targeted re-extraction and otherwise become open items.
- **Code decides what is true, under a readable policy.** Linking (same ID and issuer, otherwise
  weighted candidate links that are reported, not merged), copy detection, supersession by
  corrections, precedence (signed over unsigned over draft; timing only when every account's is
  known) and the decision of each fact (documented, corroborated, established, conflicting) are
  generic code. All domain knowledge (observation kinds, fields, precedence, service vocabulary,
  counting and goal rules) is in `record_engine/policy.toml`.
- **Temperature 0; two readings.** Every model call runs at temperature 0 except the second
  reading: each document is also read a second time as an independent sample (temperature 1); code compares every event's key fields
  between the readings. A disagreement gets one focused re-read and is settled when it agrees
  with one reading (two of three); otherwise it stays an open item. A re-read that contradicts
  both readings is rejected for its document. Where the record allows it, code derives a value
  instead of trusting wording: partial attendance from presence inside the booking, a patient's
  arrival after a patient-absent opening segment.
- **Conflicts stay open.** A conflicting value keeps every scenario; totals are computed per
  scenario and never averaged or mixed across documents.
- **Questions compile to queries.** A planner writes queries in a small query language; code
  executes them with provenance per row. The writer cites result, fact and open-item IDs and
  source lines. Code checks values, dates, goal outcomes, totals and absence claims; a small model
  checks coverage and narrative support. Code failures withhold the answer with the reasons. A
  framing step then selects and orders the checked statements that answer the question and holds
  back the rest; it never rewrites a statement.
- **The service runs the engine as durable runs** on the task queue (`analysis_tasks`,
  `analysis_results`): a record build per snapshot and a question per record, with leases,
  idempotency keys, one active run per patient and audit events. Model calls run outside
  transactions; the lease is re-checked before a result is written. Engine line citations are
  resolved to the snapshot's source spans. The worker builds each patient's latest snapshot
  automatically; extractions are cached by document content and prompt.

## Consequences

- Every fact in the record traces to quoted observations and a named rule
  (`python -m record_engine trace ID`), and the record can be exported as JSON.
- Adding a document re-extracts only that document; `python -m record_engine add` reports what
  changed in the record.
- Answer quality is bounded by the query language: a question it cannot express is answered from
  facts and passages, or withheld, never computed by the model.
- Citations cite the records behind each row an answer uses, which is broader than the minimal
  passages a reviewer needs (precision 0.61 against the benchmark's gold lines).
- A second build from nothing reproduces the episode ledger exactly; what the two readings both
  get wrong is not caught by comparing them.
- Results come from one synthetic patient and a model judge; there is no clinician review of
  facts or answers yet.
