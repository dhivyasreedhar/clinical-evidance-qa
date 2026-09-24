# Document withdrawal and restoration

## Status

Accepted, 23 Sep 2026.

## Context

Snapshots were built from every revision a patient had ever received. A document filed to the
wrong chart, or superseded by the sender, could not be taken out of the case. Two constraints
also blocked any later fix:

- A re-upload of the same bytes was treated as a duplicate and ignored.
- Snapshots were unique by manifest hash, so returning to an earlier set of documents would
  violate the constraint.

## Decision

- Source revisions stay immutable and are never deleted. Withdrawal and restoration are
  append-only `document_status_events` rows (actor, action, reason, time) with row-level
  security. The app role may insert and read them, but not update them. The latest event
  decides whether a revision is active.
- Every change goes through `set_document_status`, under the same per-patient advisory lock as
  imports. It audits `document.withdrawn` or `document.restored` and publishes a snapshot of the
  active revisions.
- Snapshots are unique by sequence only, so withdraw → restore publishes a new snapshot whose
  manifest equals an earlier one.
- Re-uploading a withdrawn document restores it.
- The worker builds the record for the new latest snapshot as usual. Unchanged documents reuse
  their cached extractions, so only linking and reconciliation rerun. A snapshot with no
  documents is not built.
- API: `POST /patients/{id}/documents/{revision}/withdraw` (a reason is required) and
  `.../restore`. The document list includes `withdrawn`. The web source viewer offers "Remove
  from case…" and lists removed documents with "Restore".

## Consequences

- Records and answers pinned to earlier snapshots stay reproducible and readable. New questions
  use the latest record, which no longer cites withdrawn records.
- Withdrawn source text remains stored for audit. Erasure (for example, a legal deletion request)
  is a separate, not-yet-built retention workflow.
