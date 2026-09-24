from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

import pytest
from clinical.application.automatic_imports import enqueue_automatic_import
from clinical.application.imports import UploadedFile, claim_job, process_job
from clinical.infrastructure.database import transaction
from clinical.infrastructure.models import Patient
from sqlalchemy import select

pytestmark = pytest.mark.integration


def record(mrn="P-1", dob="1980-01-01", name="Example Patient"):
    return f"Document ID: EXAMPLE\nPatient: {name} | DOB: {dob} | MRN: {mrn}\n\nAn original record.\n".encode()


def upload(client, files, key=None):
    response = client.post(
        "/api/v1/imports",
        headers={"Idempotency-Key": key or str(uuid4())},
        files=[("files", (name, raw, "text/plain")) for name, raw in files],
    )
    assert response.status_code == 202, response.text
    return response.json()


def process(app):
    settings = app.state.settings
    while lease := claim_job(app.state.engine, settings.dev_tenant):
        assert process_job(
            app.state.engine, app.state.store, settings.dev_tenant, lease, settings.max_file_bytes
        )


def test_packet_detects_one_patient_and_reuses_it_without_manual_creation(client, app):
    files = [(p.name, p.read_bytes()) for p in sorted(Path("documents").glob("*.txt"))]
    result = upload(client, files)
    assert not result["issues"] and len(result["jobs"]) == 1
    patients = client.get("/api/v1/patients").json()
    assert len(patients) == 1
    assert patients[0]["name"] == "Rowan Mercer"
    assert patients[0]["mrn"] == "HG-M042"
    process(app)
    assert len(client.get(f"/api/v1/patients/{patients[0]['id']}/documents").json()) == 31
    again = upload(client, files[:1])
    assert again["jobs"][0]["patient_id"] == patients[0]["id"]
    process(app)
    assert len(client.get("/api/v1/patients").json()) == 1


def test_mixed_patients_group_separately_and_unknown_file_stays_unassigned(client, app):
    result = upload(
        client,
        [
            ("one.txt", record()),
            ("two.txt", record("P-2", name="Second Patient")),
            ("unknown.txt", b"No identity here"),
        ],
    )
    assert len(result["jobs"]) == 2
    assert len({job["patient_id"] for job in result["jobs"]}) == 2
    assert result["issues"][0]["error_code"] == "identity_unconfirmed"
    process(app)
    for job in result["jobs"]:
        assert len(client.get(f"/api/v1/patients/{job['patient_id']}/documents").json()) == 1
    assert client.get("/api/v1/imports").json()[0]["issues"] == result["issues"]


def test_conflicting_dates_never_create_or_modify_patient(client, app):
    result = upload(client, [("one.txt", record()), ("two.txt", record(dob="1981-01-01"))])
    assert result["jobs"] == []
    assert len(result["issues"]) == 2
    assert client.get("/api/v1/patients").json() == []
    valid = upload(client, [("correct.txt", record())])
    invalid = upload(client, [("conflict.txt", record(dob="1981-01-01"))])
    assert invalid["jobs"] == []
    assert invalid["issues"][0]["error_code"] == "conflicting_identifiers"
    assert client.get("/api/v1/patients").json()[0]["birth_date"] == "1980-01-01"
    assert len(valid["jobs"]) == 1


def test_automatic_routing_cannot_grant_access_to_existing_patient(client, app):
    upload(client, [("one.txt", record())])
    app.state.settings.dev_actor = uuid4()
    client.headers["X-CSRF-Token"] = client.post("/api/v1/dev-session").json()["csrf_token"]
    result = upload(client, [("one.txt", record())])
    assert result["jobs"] == []
    assert result["issues"][0]["error_code"] == "identity_review_required"
    assert client.get("/api/v1/patients").json() == []


def test_idempotency_and_simultaneous_new_patient_detection(client, app):
    settings = app.state.settings
    key = str(uuid4())

    def enqueue(_):
        with transaction(app.state.engine, settings.dev_tenant) as db:
            return enqueue_automatic_import(
                db,
                app.state.store,
                settings.dev_tenant,
                settings.dev_actor,
                key,
                (UploadedFile("one.txt", record()),),
                settings.max_file_bytes,
            ).id

    with ThreadPoolExecutor(max_workers=2) as pool:
        ids = list(pool.map(enqueue, range(2)))
    assert ids[0] == ids[1]
    assert len(client.get("/api/v1/patients").json()) == 1
    assert len(client.get("/api/v1/imports").json()) == 1
    response = client.post(
        "/api/v1/imports",
        headers={"Idempotency-Key": key},
        files=[("files", ("different.txt", record("P-2"), "text/plain"))],
    )
    assert response.status_code == 409


def test_archived_cases_are_hidden_and_cannot_be_silently_reopened(client, app):
    result = upload(client, [("one.txt", record())])
    with transaction(app.state.engine, app.state.settings.dev_tenant) as db:
        patient = db.scalar(select(Patient))
        patient.archived = True
    assert client.get("/api/v1/patients").json() == []
    assert (
        client.get(f"/api/v1/patients/{result['jobs'][0]['patient_id']}/documents").status_code
        == 404
    )
    assert upload(client, [("one.txt", record())])["jobs"] == []
    history = client.get("/api/v1/imports")
    assert history.status_code == 200
    assert all(not batch["jobs"] for batch in history.json())
