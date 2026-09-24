# ADR 0001: source-first local vertical slice

Status: accepted for local synthetic-data development, 2026-09-22.

The initial increment proves source fidelity and durable ingestion before inference.
Domain evidence modules have no web, ORM, or model dependencies. FastAPI
coordinates use cases; SQLAlchemy maps persistence; the Next.js app consumes generated
OpenAPI types. Runtime code never imports planning answers or evaluation fixtures.

PostgreSQL is authoritative. The application uses a non-owner, non-superuser role
without BYPASSRLS. Transaction-local tenant scope and forced row-level security protect
every table; patient grants are checked separately in application use cases. Source
revisions, spans, snapshots, and audit events are insert-only for the runtime role.
Changes to source bytes create a separate revision; duplicate upload provenance remains
in the import history. A changed declared document ID does not establish supersession.
Both versions stay in source manifests; the record engine reconciles what they say (ADR 0003).

For this increment, the PostgreSQL jobs table is the durable queue. There is no dual
write or external broker, so no outbox dispatcher is necessary yet. SKIP LOCKED claims,
expiring leases, attempt tokens, bounded attempts, and short atomic transactions support
recovery. Patient-scoped advisory locks serialize snapshot construction. Three failed
claims produce a visible terminal failure. Successful processing can contain quarantined
or invalid files; those dispositions and incomplete source coverage remain visible.

Model stages do not inherit the short-transaction processing pattern: record builds and
answers run outside transactions, renew their leases, and publish with fencing (ADR 0003). An
external queue, when introduced, needs a transactional outbox and idempotent consumers.

Source snapshots enumerate exact revisions and hashes, and are explicitly labeled
sources-only. They are not validated clinical abstractions. Structural paragraphs are
inspectable. Clinical interpretation happens only in the record engine, over a pinned
snapshot (ADR 0003).

Private local files implement the ObjectStore port. Temporary writes are fsynced and
atomically linked; reads verify their digest. Production object storage and lifecycle
cleanup are pending. Orphaned staged objects after a database rollback are an accepted
local limitation; they are never referenced by accepted jobs.

Authentication is an explicitly shared synthetic development identity in an expiring,
signed HttpOnly/SameSite session. Mutation requests require a configured loopback Origin
and CSRF token. Non-development configurations fail at startup. This is not OIDC and
must not be deployed for real records. The next foundation increment must add OIDC,
server-managed session revocation, service identities, authorized review of quarantined
files, managed storage, and broader operational controls.

Source text stays exact UTF-8, including CRLF and BOM. Citation offsets are Unicode code
points; line numbers follow Python splitlines. UI highlighting uses server-provided line
numbers, avoiding JavaScript UTF-16 offset differences. Clinical calculations are done by code
in the record engine (ADR 0003); conflicting values stay discrete scenarios. No
patient-specific threshold is encoded anywhere.

Relevant implementation references: [FastAPI lifecycle](https://fastapi.tiangolo.com/advanced/events/),
[PostgreSQL row security](https://www.postgresql.org/docs/16/ddl-rowsecurity.html),
[Next.js installation](https://nextjs.org/docs/app/getting-started/installation).
