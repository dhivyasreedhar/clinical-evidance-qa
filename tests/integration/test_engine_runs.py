from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from clinical.application import engine_runs
from clinical.application.engine_runs import (
    claim_run,
    enqueue_latest_records,
    process_run,
    release_run,
    renew_lease,
)
from clinical.infrastructure.database import transaction
from clinical.infrastructure.models import AnalysisTask
from pydantic import SecretStr
from test_ingestion import create_patient, process, upload

pytestmark = pytest.mark.integration


def published_answer(qid, question, record, policy, index=None):
    """Stands in for the model-backed answer step; cites the source's statement line."""
    return {
        "id": qid,
        "question": question,
        "status": "answered",
        "answer": {
            "statements": [{"text": "A statement.", "kind": "fact", "cites": ["source:L4"]}]
        },
        "results": [],
        "reasons": [],
    }


class FakeEngine:
    """The engine's model-backed steps; reconciliation, queries and rendering run for real."""

    def __init__(self):
        self.extracted: list[str] = []

    def observe_checked(self, documents, policy, workers=6):
        self.extracted += [d.filename for d in documents]
        return [], [], {}


@pytest.fixture
def fake(monkeypatch):
    engine = FakeEngine()
    monkeypatch.setattr(engine_runs, "observe_checked", engine.observe_checked)
    monkeypatch.setattr(engine_runs, "answer_question", published_answer)
    return engine


def setup_case(client, app):
    patient = create_patient(client)
    upload(client, patient)
    process(app)
    snapshot = client.get(f"/api/v1/patients/{patient}/snapshots").json()[0]
    app.state.settings.anthropic_api_key = SecretStr("test-placeholder-no-network")
    return patient, snapshot


def post(client, patient, path, body, key=None):
    return client.post(
        f"/api/v1/patients/{patient}/{path}",
        headers={"Idempotency-Key": key or str(uuid4())},
        json=body,
    )


def work(app):
    settings = app.state.settings
    lease = claim_run(app.state.engine, settings.dev_tenant)
    assert lease
    process_run(app.state.engine, settings, settings.dev_tenant, lease)
    return lease


def runs(client, patient):
    return client.get(f"/api/v1/patients/{patient}/runs").json()


def test_record_build_view_export_and_cited_answer(client, app, fake):
    patient, snapshot = setup_case(client, app)
    key = str(uuid4())
    response = post(client, patient, "records", {"snapshot_id": snapshot["id"]}, key)
    assert response.status_code == 202, response.text
    run = response.json()
    assert run["kind"] == "engine_record" and run["status"] == "queued"
    replay = post(client, patient, "records", {"snapshot_id": snapshot["id"]}, key)
    assert replay.json()["id"] == run["id"]
    # a question needs a finished record
    early = post(client, patient, "answers", {"record_id": run["id"], "question": "What?"})
    assert early.status_code == 409 and early.json()["detail"] == "engine_record_required"
    version = client.get(f"/api/v1/patients/{patient}/runs/version").json()["version"]

    work(app)
    assert client.get(f"/api/v1/patients/{patient}/runs/version").json()["version"] != version
    detail = client.get(f"/api/v1/patients/{patient}/runs/{run['id']}").json()
    assert detail["status"] == "succeeded" and detail["answer"] is None
    view = detail["record"]
    assert view["encounters"] == [] and view["totals"] is None
    assert [d["filename"] for d in view["documents"]] == ["source.txt"]
    assert view["documents"][0]["revision_id"] == snapshot["manifest"][0]["revision_id"]
    assert detail["usage"]["calls"] == 0
    exported = client.get(f"/api/v1/patients/{patient}/records/{run['id']}/export")
    assert exported.status_code == 200 and exported.json()["documents"][0]["key"] == "source"
    assert "attachment" in exported.headers["content-disposition"]
    markdown = client.get(
        f"/api/v1/patients/{patient}/records/{run['id']}/export", params={"format": "markdown"}
    )
    assert markdown.text.startswith("# Clinical abstraction")

    question = post(client, patient, "answers", {"record_id": run["id"], "question": "What?"})
    assert question.status_code == 202, question.text
    assert question.json()["record_id"] == run["id"]
    work(app)
    answer = client.get(f"/api/v1/patients/{patient}/runs/{question.json()['id']}").json()
    assert answer["status"] == "succeeded"
    statement = answer["answer"]["statements"][0]
    assert statement["text"] == "A statement."
    assert [c["quote"] for c in statement["citations"]] == ["A source statement."]
    assert [r["kind"] for r in runs(client, patient)] == ["engine_answer", "engine_record"]
    # an answer run has no record to export
    other = client.get(f"/api/v1/patients/{patient}/records/{question.json()['id']}/export")
    assert other.status_code == 404


def test_failed_build_is_visible_and_answers_are_refused(client, app, monkeypatch):
    patient, snapshot = setup_case(client, app)

    def broken(documents, policy, workers=6):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(engine_runs, "observe_checked", broken)
    run = post(client, patient, "records", {"snapshot_id": snapshot["id"]}).json()
    work(app)
    detail = client.get(f"/api/v1/patients/{patient}/runs/{run['id']}").json()
    assert detail["status"] == "failed" and detail["error_code"] == "engine_processing_failed"
    assert detail["record"] is None
    refused = post(client, patient, "answers", {"record_id": run["id"], "question": "What?"})
    assert refused.status_code == 409


def test_expired_lease_fences_model_calls_and_publication(client, app, fake):
    patient, snapshot = setup_case(client, app)
    post(client, patient, "records", {"snapshot_id": snapshot["id"]})
    settings = app.state.settings
    first = claim_run(app.state.engine, settings.dev_tenant)
    with transaction(app.state.engine, settings.dev_tenant) as db:
        db.get(AnalysisTask, first.task_id).lease_until = datetime.now(UTC) - timedelta(seconds=1)
    second = claim_run(app.state.engine, settings.dev_tenant)
    process_run(app.state.engine, settings, settings.dev_tenant, first)
    assert fake.extracted == []
    process_run(app.state.engine, settings, settings.dev_tenant, second)
    assert fake.extracted == ["source.txt"]
    assert runs(client, patient)[0]["status"] == "succeeded"


def test_a_stopped_workers_run_is_resumed_and_its_result_fenced(client, app, fake):
    patient, snapshot = setup_case(client, app)
    post(client, patient, "records", {"snapshot_id": snapshot["id"]})
    settings = app.state.settings
    stopped = claim_run(app.state.engine, settings.dev_tenant)
    assert renew_lease(app.state.engine, settings.dev_tenant, stopped, 120)
    # the worker stops mid-build: the run goes back to the queue, not counted as an attempt
    release_run(app.state.engine, settings.dev_tenant, stopped)
    assert runs(client, patient)[0]["status"] == "queued"
    assert not renew_lease(app.state.engine, settings.dev_tenant, stopped, 120)
    resumed = claim_run(app.state.engine, settings.dev_tenant)
    assert resumed and resumed.token != stopped.token
    with transaction(app.state.engine, settings.dev_tenant) as db:
        assert db.get(AnalysisTask, resumed.task_id).attempt == 1
    # the stopped worker's build cannot publish; the resumed one does
    process_run(app.state.engine, settings, settings.dev_tenant, stopped)
    assert fake.extracted == []
    process_run(app.state.engine, settings, settings.dev_tenant, resumed)
    assert runs(client, patient)[0]["status"] == "succeeded"


def test_key_presence_scope_and_patient_access(client, app, fake):
    patient, snapshot = setup_case(client, app)
    app.state.settings.anthropic_api_key = SecretStr("")
    response = post(client, patient, "records", {"snapshot_id": snapshot["id"]})
    assert response.json()["detail"] == "claude_key_missing"
    app.state.settings.anthropic_api_key = SecretStr("test")
    missing = post(client, patient, "answers", {"record_id": str(uuid4()), "question": "What?"})
    assert missing.status_code == 404
    other = client.post(
        "/api/v1/patients",
        json={"name": "Other Example", "mrn": "TEST-2", "birth_date": "1981-02-03"},
    ).json()["id"]
    assert post(client, other, "records", {"snapshot_id": snapshot["id"]}).status_code == 404
    run = post(client, patient, "records", {"snapshot_id": snapshot["id"]}).json()
    assert client.get(f"/api/v1/patients/{other}/runs/{run['id']}").status_code == 404
    app.state.settings.dev_actor = uuid4()
    login = client.post("/api/v1/dev-session").json()
    client.headers["X-CSRF-Token"] = login["csrf_token"]
    assert client.get(f"/api/v1/patients/{patient}/runs").status_code == 404
    assert post(client, patient, "records", {"snapshot_id": snapshot["id"]}).status_code == 404


def test_new_snapshot_is_built_automatically_once(client, app, fake):
    patient, first = setup_case(client, app)
    settings = app.state.settings
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    assert [r["snapshot_id"] for r in runs(client, patient)] == [first["id"]]
    lease = claim_run(app.state.engine, settings.dev_tenant)
    upload(client, patient, raw=b"MRN: TEST-1 | DOB: 1980-02-03\nAnother document")
    process(app)
    latest = client.get(f"/api/v1/patients/{patient}/snapshots").json()[0]
    # one run per patient at a time: the new snapshot waits for the running build
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    assert len(runs(client, patient)) == 1
    process_run(app.state.engine, settings, settings.dev_tenant, lease)
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    current = [r for r in runs(client, patient) if r["snapshot_id"] == latest["id"]]
    assert len(current) == 1 and current[0]["status"] == "queued"
    work(app)
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    assert len(runs(client, patient)) == 2


def test_withdrawn_documents_leave_the_record_and_an_empty_case_is_skipped(client, app, fake):
    patient, first = setup_case(client, app)
    settings = app.state.settings
    upload(client, patient, raw=b"MRN: TEST-1 | DOB: 1980-02-03\nAnother document")
    process(app)
    documents = client.get(f"/api/v1/patients/{patient}/documents").json()
    extra = next(
        d["id"] for d in documents if d["id"] not in {r["revision_id"] for r in first["manifest"]}
    )
    response = client.post(
        f"/api/v1/patients/{patient}/documents/{extra}/withdraw", json={"reason": "wrong chart"}
    )
    assert response.status_code == 200
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    run = runs(client, patient)[0]
    assert run["snapshot_id"] == response.json()["snapshot_id"]
    work(app)
    view = client.get(f"/api/v1/patients/{patient}/runs/{run['id']}").json()["record"]
    assert [d["revision_id"] for d in view["documents"]] == [first["manifest"][0]["revision_id"]]
    for document in client.get(f"/api/v1/patients/{patient}/documents").json():
        if not document["withdrawn"]:
            client.post(
                f"/api/v1/patients/{patient}/documents/{document['id']}/withdraw",
                json={"reason": "empty the case"},
            )
    before = len(runs(client, patient))
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    assert len(runs(client, patient)) == before


def test_a_record_from_another_engine_version_is_rebuilt_and_not_answered_over(
    client, app, fake, monkeypatch
):
    import clinical.api.main as api

    patient, snapshot = setup_case(client, app)
    settings = app.state.settings
    run = post(client, patient, "records", {"snapshot_id": snapshot["id"]}).json()
    work(app)
    # the engine is upgraded after the record was built
    upgraded = ("record-engine-next:" + engine_runs.EXTRACT_VERSION, engine_runs.versions()[1])
    monkeypatch.setattr(engine_runs, "versions", lambda: upgraded)
    monkeypatch.setattr(api, "versions", lambda: upgraded)
    refused = post(client, patient, "answers", {"record_id": run["id"], "question": "What?"})
    assert refused.status_code == 409 and refused.json()["detail"] == "record_outdated"
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    builds = [r for r in runs(client, patient) if r["kind"] == "engine_record"]
    assert [r["status"] for r in builds] == ["queued", "succeeded"]
    assert (
        builds[0]["prompt_version"] == client.get("/api/v1/model-status").json()["engine_version"]
    )


def test_a_policy_change_alone_also_rebuilds_the_record(client, app, fake, monkeypatch):
    import clinical.api.main as api

    patient, snapshot = setup_case(client, app)
    settings = app.state.settings
    post(client, patient, "records", {"snapshot_id": snapshot["id"]})
    work(app)
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    assert len(runs(client, patient)) == 1
    upgraded = (engine_runs.versions()[0], "policy-next")
    monkeypatch.setattr(engine_runs, "versions", lambda: upgraded)
    monkeypatch.setattr(api, "versions", lambda: upgraded)
    enqueue_latest_records(app.state.engine, settings, settings.dev_tenant)
    builds = [r for r in runs(client, patient) if r["kind"] == "engine_record"]
    assert [r["status"] for r in builds] == ["queued", "succeeded"]
    assert builds[0]["schema_version"] == "policy-next"
