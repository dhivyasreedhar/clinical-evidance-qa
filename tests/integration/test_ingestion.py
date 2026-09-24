from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from clinical.application.imports import UploadedFile, claim_job, enqueue_import, process_job
from clinical.infrastructure.database import transaction
from clinical.infrastructure.models import Job, Patient, Revision
from sqlalchemy import select, text
from sqlalchemy.exc import DBAPIError

pytestmark = pytest.mark.integration
RAW = b"Document ID: SYN-1\r\nPatient: Fictional | MRN: TEST-1 | DOB: 1980-02-03\r\n\r\nA source statement.\r\n"


def create_patient(client):
    response = client.post(
        "/api/v1/patients",
        json={"name": "Fictional Example", "mrn": "TEST-1", "birth_date": "1980-02-03"},
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def upload(client, patient, raw=RAW, key=None, filename="source.txt"):
    return client.post(
        f"/api/v1/patients/{patient}/imports",
        headers={"Idempotency-Key": key or str(uuid4())},
        files=[("files", (filename, raw, "text/plain"))],
    )


def process(app):
    settings = app.state.settings
    lease = claim_job(app.state.engine, settings.dev_tenant)
    assert lease
    assert process_job(
        app.state.engine, app.state.store, settings.dev_tenant, lease, settings.max_file_bytes
    )
    return lease


def test_import_replay_duplicate_and_exact_citation(client, app):
    patient = create_patient(client)
    key = str(uuid4())
    first = upload(client, patient, key=key)
    assert first.status_code == 202, first.text
    assert first.json()["status"] == "queued"
    replay = upload(client, patient, key=key)
    assert replay.json()["id"] == first.json()["id"]
    assert upload(client, patient, raw=RAW + b"changed", key=key).status_code == 409
    process(app)
    docs = client.get(f"/api/v1/patients/{patient}/documents").json()
    assert len(docs) == 1
    source = client.get(f"/api/v1/source-revisions/{docs[0]['id']}").json()
    assert source["text"].encode() == RAW
    for span in source["spans"]:
        assert source["text"][span["start_char"] : span["end_char"]] == span["quote"]
        assert (
            client.get(f"/api/v1/source-revisions/{source['id']}/spans/{span['id']}").status_code
            == 200
        )
    upload(client, patient, filename="renamed.txt")
    process(app)
    jobs = client.get(f"/api/v1/patients/{patient}/jobs").json()
    assert sorted(j["uploads"][0]["status"] for j in jobs) == ["accepted", "duplicate"]
    snapshots = client.get(f"/api/v1/patients/{patient}/snapshots").json()
    assert len(snapshots) == 1


def test_changed_content_retains_historical_snapshot(client, app):
    patient = create_patient(client)
    upload(client, patient)
    process(app)
    old = client.get(f"/api/v1/patients/{patient}/snapshots").json()[0]
    upload(client, patient, raw=RAW + b"New source account.")
    process(app)
    snapshots = client.get(f"/api/v1/patients/{patient}/snapshots").json()
    assert [len(s["manifest"]) for s in snapshots] == [2, 1]
    assert snapshots[1] == old


@pytest.mark.parametrize(
    "raw,filename,status",
    [
        (RAW.replace(b"TEST-1", b"OTHER"), "note.txt", "quarantined"),
        (b"No identifiers", "note.txt", "quarantined"),
        (b"\xff", "note.txt", "failed"),
        (RAW, "note.pdf", "failed"),
    ],
)
def test_rejected_inputs_have_visible_dispositions(client, app, raw, filename, status):
    patient = create_patient(client)
    response = upload(client, patient, raw=raw, filename=filename)
    process(app)
    job = client.get(f"/api/v1/jobs/{response.json()['id']}").json()
    assert job["uploads"][0]["status"] == status
    assert client.get(f"/api/v1/patients/{patient}/documents").json() == []


def test_expired_lease_recovery_fences_stale_worker(client, app):
    patient = create_patient(client)
    upload(client, patient)
    tenant = app.state.settings.dev_tenant
    first = claim_job(app.state.engine, tenant)
    assert first
    with transaction(app.state.engine, tenant) as db:
        job = db.get(Job, first.job_id)
        job.lease_until = datetime.now(UTC) - timedelta(seconds=1)
    second = claim_job(app.state.engine, tenant)
    assert second and second.token != first.token
    assert not process_job(app.state.engine, app.state.store, tenant, first, 10000)
    assert process_job(app.state.engine, app.state.store, tenant, second, 10000)


def test_tenant_rls_pool_reuse_and_immutable_evidence(client, app):
    patient = create_patient(client)
    upload(client, patient)
    process(app)
    tenant = app.state.settings.dev_tenant
    with transaction(app.state.engine, tenant) as db:
        role = db.execute(
            text("SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = current_user")
        ).one()
        assert role == (False, False)
        assert len(db.scalars(select(Revision)).all()) == 1
    with transaction(app.state.engine, uuid4()) as db:
        assert db.scalars(select(Patient)).all() == []
        assert db.scalars(select(Revision)).all() == []
    with app.state.engine.connect() as connection:
        assert connection.execute(text("SELECT count(*) FROM document_revisions")).scalar() == 0
    with pytest.raises(DBAPIError), transaction(app.state.engine, tenant) as db:
        db.execute(text("UPDATE document_revisions SET text = 'tampered'"))
    with pytest.raises(DBAPIError), transaction(app.state.engine, tenant) as db:
        db.execute(text("DELETE FROM audit_events"))


def test_patient_access_and_csrf_are_required(client, app):
    patient = create_patient(client)
    tenant = app.state.settings.dev_tenant
    with transaction(app.state.engine, tenant) as db:
        hidden = Patient(
            tenant_id=tenant,
            name="Not granted",
            mrn="HIDDEN",
            birth_date=datetime(1980, 1, 1).date(),
        )
        db.add(hidden)
        db.flush()
        hidden_id = hidden.id
    assert client.get(f"/api/v1/patients/{hidden_id}/documents").status_code == 404
    assert upload(client, hidden_id).status_code == 404
    assert (
        client.post("/api/v1/patients", headers={"X-CSRF-Token": "bad"}, json={}).status_code == 403
    )
    assert (
        client.post("/api/v1/dev-session", headers={"Origin": "https://evil.example"}).status_code
        == 403
    )
    client.cookies.clear()
    assert client.get(f"/api/v1/patients/{patient}/documents").status_code == 401


def test_concurrent_idempotent_submissions_create_one_job(client, app):
    patient = UUID(create_patient(client))
    settings = app.state.settings
    key = str(uuid4())

    def submit():
        with transaction(app.state.engine, settings.dev_tenant) as db:
            return enqueue_import(
                db,
                app.state.store,
                settings.dev_tenant,
                settings.dev_actor,
                patient,
                key,
                (UploadedFile("source.txt", RAW),),
            ).id

    with ThreadPoolExecutor(max_workers=2) as pool:
        ids = list(pool.map(lambda _: submit(), range(2)))
    assert ids[0] == ids[1]


def test_supplied_packet_imports_all_sources_without_runtime_case_logic(client, app):
    response = client.post(
        "/api/v1/patients",
        json={"name": "Rowan Mercer", "mrn": "HG-M042", "birth_date": "1991-04-12"},
    )
    patient = response.json()["id"]
    files = sorted(Path("documents").glob("*.txt"))
    result = client.post(
        f"/api/v1/patients/{patient}/imports",
        headers={"Idempotency-Key": str(uuid4())},
        files=[("files", (f.name, f.read_bytes(), "text/plain")) for f in files],
    )
    assert result.status_code == 202
    process(app)
    docs = client.get(f"/api/v1/patients/{patient}/documents").json()
    assert len(docs) == 31
    assert sum(doc["line_count"] for doc in docs) == 535


def test_concurrent_imports_publish_cumulative_snapshots(client, app):
    patient = create_patient(client)
    upload(client, patient)
    upload(client, patient, raw=RAW + b"Another independent source account.")
    tenant = app.state.settings.dev_tenant
    first = claim_job(app.state.engine, tenant)
    second = claim_job(app.state.engine, tenant)
    assert first and second and first.job_id != second.job_id
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(
            pool.map(
                lambda lease: process_job(app.state.engine, app.state.store, tenant, lease, 10000),
                (first, second),
            )
        )
    assert results == [True, True]
    snapshots = client.get(f"/api/v1/patients/{patient}/snapshots").json()
    assert [len(s["manifest"]) for s in snapshots] == [2, 1]


def test_guessed_source_job_and_citation_ids_require_patient_grant(client, app):
    patient = create_patient(client)
    job = upload(client, patient).json()
    process(app)
    revision = client.get(f"/api/v1/patients/{patient}/documents").json()[0]
    source = client.get(f"/api/v1/source-revisions/{revision['id']}").json()
    # A different actor in the same tenant has no patient grants.
    app.state.settings.dev_actor = uuid4()
    signed_in = client.post("/api/v1/dev-session").json()
    client.headers["X-CSRF-Token"] = signed_in["csrf_token"]
    assert client.get("/api/v1/patients").json() == []
    assert client.get(f"/api/v1/jobs/{job['id']}").status_code == 404
    assert client.get(f"/api/v1/source-revisions/{revision['id']}").status_code == 404
    assert (
        client.get(
            f"/api/v1/source-revisions/{revision['id']}/spans/{source['spans'][0]['id']}"
        ).status_code
        == 404
    )
