# Operations guide

Setup, the web application, the API, configuration and verification in detail. The project
overview, results and evaluation are in the [README](../README.md).

## Run the web application locally

Requirements: Node 24, Python 3.13, uv, and Docker Compose with a running Docker daemon.
Python and Node dependencies are locked in `uv.lock` and `package-lock.json`.

```sh
make setup
make db
make migrate
make dev
```

Open **http://localhost:3000** and select **Enter development workspace**. Choose the
TXT documents and import them. The app detects MRN and birth date, creates or reuses
the matching patient, and opens the case automatically. No manual patient creation is
needed. All 31 supplied documents group into Rowan Mercer’s case. A patient selector
appears only when more than one active patient exists. Upload routing always uses the
file’s identity, independently of whichever case is currently open.
Click a source to read it; select a source block to highlight its exact citation.
Repeated uploads retain their import provenance without multiplying source revisions.
To take a document out of a case (for example, one filed to the wrong chart), open it and choose
**Remove from case…** with a reason. The original stays preserved for audit, a new snapshot without
it is published and its record is rebuilt automatically, and it can be restored from **Removed from
case** (or by uploading it again). Files for a new patient are routed by MRN and date of birth into
their own case automatically (ADR 0002).

To use Claude, add `EHR_ANTHROPIC_API_KEY` to the local `.env` and restart `make dev`. The key
stays on the server. After an upload is processed, the worker builds the record for the new
snapshot. Each document's extraction is cached by its content, so a rebuild after an import pays
only for the new documents. Import processing stays responsive while a build runs, and uploads
made during a build are picked up when it finishes.

- **Clinical record** shows what code computed from the record: sessions, treatment days and
  minutes, the weekly goal result per threshold, the encounter ledger, open items that need review
  (conflicts, candidate links, uncovered mentions, documents set aside), every fact of every event
  with its status and rule, and the clinical findings by date. Values the sources disagree about
  keep every possibility ("40 or 50 min"). Every value links to its source lines. The record can
  be downloaded as JSON (every fact with its evidence) or as a readable abstraction.
- **Documents** lists each document's title, issuer, the service dates it supports, and whether it
  is a copy of another document or was set aside (for example, another patient's note).
- **Ask a question** answers over the record, on point: the direct answer first, then only what
  is needed to read it (a conflict or gap about the figure asked). Checked details the question
  did not ask about sit under **Other details from the record**. Every statement cites source
  lines; answers that fail a check are withheld with the reasons, and answers with coverage gaps
  are marked partial.

`make dev` starts the web app, API on `127.0.0.1:8008`, and worker. Ctrl-C stops those
processes; database data persists. Logs are in `.local/logs`. API docs are at
http://127.0.0.1:8008/docs. Database migrations run explicitly, never on API startup.
Use `docker compose -f infra/compose.yaml stop` to stop the development database.

If Docker is unavailable, a separately installed PostgreSQL 16 server can use a
project-local data directory on the same port. Do not run initialization again against
existing data:

```sh
initdb -D .local/postgres -U ehr_owner --auth-local=trust --auth-host=trust --locale=C --encoding=UTF8
pg_ctl -D .local/postgres -l .local/postgres.log -o '-h 127.0.0.1 -p 55432 -k /tmp' start
psql -h 127.0.0.1 -p 55432 -U ehr_owner -d postgres -v ON_ERROR_STOP=1 -f infra/bootstrap.sql
make migrate
make dev
```

That trust-authenticated fallback is for this isolated, loopback-only synthetic setup.
It must not be used on shared hosts. Stop it with `pg_ctl -D .local/postgres stop`.
Do not run Compose and the native database on port 55432 simultaneously.

## API

Record builds and questions are durable runs on a database queue with leases, idempotency keys,
one active run per patient, and audit events. Model calls run outside database transactions, and
the lease is re-checked before a result is written.

| Method | Path | |
|---|---|---|
| POST | `/api/v1/patients/{patient_id}/records` | build the record for a snapshot (`Idempotency-Key` header) |
| POST | `/api/v1/patients/{patient_id}/answers` | ask a question over a built record |
| GET | `/api/v1/patients/{patient_id}/runs` | runs, newest first |
| GET | `/api/v1/patients/{patient_id}/runs/version` | change marker for polling |
| GET | `/api/v1/patients/{patient_id}/runs/{run_id}` | a run with its record view or cited answer |
| GET | `/api/v1/patients/{patient_id}/records/{run_id}/export` | the full record (`format=json`) or abstraction (`format=markdown`) |

The engine's line citations are resolved to the snapshot's source spans, the same citations the
source viewer highlights. `services/` holds the service and the repository root holds
`record_engine`; both must be on `PYTHONPATH` (`make dev` sets them).

## Configuration and boundaries

`make setup` creates `.env` with a random session secret and preserves an existing
file. `.env`, caches, local database, objects, and logs are ignored. `.env.example`
documents the service's `EHR_` settings. Important settings:

- `EHR_DATABASE_URL`: restricted non-owner runtime database role.
- `EHR_MIGRATION_DATABASE_URL`: migration owner, never used by API/worker transactions.
- `EHR_OBJECT_ROOT`: private local content-addressed object directory.
- `EHR_SESSION_SECRET`: at least 32 characters; generated locally, never a browser value.
- `EHR_BROWSER_ORIGIN`: defaults to `http://localhost:3000`; use that exact browser URL.
- `EHR_DEV_TENANT` / `EHR_DEV_ACTOR`: shared fictional development identity.
- `EHR_ENVIRONMENT`: only `development` and `test` accepted. Production startup is disabled.
- `EHR_ANTHROPIC_API_KEY`: server-only Anthropic key; never a `NEXT_PUBLIC` setting.
- `EHR_RUN_CONCURRENCY`: runs for different patients processed at once by one worker (default 2).
- `EHR_RUN_LEASE_SECONDS`: abandoned-worker recovery window (default 120). A running build renews
  its lease every quarter lease; a worker that stops hands its unfinished runs back to the queue,
  and they resume from the model cache when the worker starts again.
- `RECORD_ENGINE_WRITER` / `RECORD_ENGINE_PLANNER` / `RECORD_ENGINE_SMALL`: the engine's models
  (defaults `claude-sonnet-4-6`, the writer, `claude-haiku-4-5-20251001`);
  `RECORD_ENGINE_CACHE`: model output cache (default `.local/record_engine/cache`). These are read
  from the process environment, not from `.env`.

The application never automatically reads `documents/` or the benchmark answer keys.
All imports enter through the same API. Source blocks describe structural paragraphs, not
clinical interpretations. Source snapshots are source-only manifests; each run pins a snapshot.
A processing-complete job can have quarantined/failed files; inspect its per-file dispositions.
Non-TXT files, invalid UTF-8, and unknown/mismatched header identities never enter an accepted
snapshot. Automatic imports retain unassigned files with missing/conflicting identities in an
actor-scoped review list; they never borrow another file’s identity. Distinct MRNs are
grouped separately. A single MRN with incompatible birth dates is held for review.
Existing patient access grants remain required; uploads cannot grant access to another
user’s case. Archived test cases remain auditable but are hidden from the active list.
Limits: 100 files/import, 10 MiB/file, 25 MiB total; request-length metadata is required.

## Evaluation

```sh
make evaluate    # record + 65 questions + judge + metrics + stability -> submission/ (paid, cached)
make heldout     # 15 held-out questions, graded separately
make scenarios   # 13 changed-input scenarios
```

`record_engine.evaluate score` computes the deterministic metrics without model calls:
publication, citation-set precision/recall/F1 against the gold source lines, exact calculations,
and BLEU/ROUGE as secondary diagnostics. The gold file is read only by the evaluator. Results
are in [submission/benchmark/README.md](../submission/benchmark/README.md).

## Verification

```sh
make check
make test
make integration
npm run build
make contracts
PLAYWRIGHT_BROWSERS_PATH=.cache/playwright npx playwright install chromium
# Starts/stops isolated test services automatically:
make browser
```

`make test` runs the unit tests and the engine's offline tests (no model calls). Integration
tests use only `ehr_test`, with new tenant/actor IDs per test. They exercise real PostgreSQL,
including forced RLS with a non-owner role, immutable evidence/audit permissions, exact
text/quotes, idempotency under concurrency, historical snapshots, expired-lease fencing, missing
identities, the complete 31-file packet, and record builds and answers with the engine's model
steps replaced by fakes. No clinical expected answers are injected into inference.

OpenAPI and TypeScript schemas are generated by `make contracts`; CI checks for drift.
Browser tests start isolated services on ports 3001/8009, use `ehr_test`, fresh tenant
and actor IDs, separate object storage, and a separate Next.js build directory. They
never seed fixtures into the working app database or reuse a running app. They verify
uploads, citations, duplicates, patient selection across refresh, the record, documents and
answer views, and mobile layout. Test databases should be periodically recreated by their owner.

## Limitations

Workers take patient-scoped transactional advisory locks, so they need no patient-table
update grant; source and audit mutation permissions remain denied. Concurrency regressions guard
idempotent submission and cumulative snapshots; same-tenant grant checks cover guessed
job, source, and citation IDs. Mid-run access revocation remains a planned fault test.

Identity gating recognizes explicit `MRN` and ISO `DOB` headers. Records without them are
quarantined even if a clinician could infer identity. The record's facts are decided by written
rules, not reviewed by a clinician; there is no reviewer sign-off on facts or answers yet.

The development identity is shared, sign-out clears the cookie without server-side
revocation, and local filesystem storage is not a production object store. There is no
managed queue/outbox, file-disposition review/retry UI, full audit coverage, retention
cleanup, reviewer sign-off, or clinical release evidence yet.

Build, fake-provider tests and live runs are engineering checks, not a clinical validation study.
