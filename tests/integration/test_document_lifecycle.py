from uuid import uuid4

import pytest
from test_automatic_import import process, record, upload

pytestmark = pytest.mark.integration


def note(text: str, mrn: str = "P-1", name: str = "Example Patient") -> bytes:
    return record(mrn=mrn, name=name) + text.encode()


def latest(client, patient_id):
    return client.get(f"/api/v1/patients/{patient_id}/snapshots").json()[0]


def manifest_ids(snapshot):
    return {row["revision_id"] for row in snapshot["manifest"]}


def test_add_withdraw_restore_and_reupload(client, app):
    result = upload(client, [("a.txt", note("first")), ("b.txt", note("second"))])
    process(app)
    patient_id = result["jobs"][0]["patient_id"]
    first = latest(client, patient_id)
    assert len(first["manifest"]) == 2

    # Adding a document publishes a new snapshot containing it.
    upload(client, [("c.txt", note("third"))])
    process(app)
    added = latest(client, patient_id)
    assert added["sequence"] == first["sequence"] + 1 and len(added["manifest"]) == 3
    docs = {d["filename"]: d for d in client.get(f"/api/v1/patients/{patient_id}/documents").json()}
    target = docs["c.txt"]["id"]

    # Withdrawing publishes a snapshot without it; the source stays readable for audit.
    path = f"/api/v1/patients/{patient_id}/documents/{target}"
    response = client.post(f"{path}/withdraw", json={"reason": "Filed to the wrong chart"})
    assert response.status_code == 200, response.text
    assert response.json()["withdrawn"] is True
    removed = latest(client, patient_id)
    assert removed["id"] == response.json()["snapshot_id"]
    assert manifest_ids(removed) == manifest_ids(first)
    assert removed["sequence"] == added["sequence"] + 1
    listed = {d["id"]: d for d in client.get(f"/api/v1/patients/{patient_id}/documents").json()}
    assert listed[target]["withdrawn"] is True
    assert client.get(f"/api/v1/source-revisions/{target}").status_code == 200
    assert client.post(f"{path}/withdraw", json={"reason": "again"}).status_code == 409
    assert client.post(f"{path}/withdraw", json={"reason": ""}).status_code == 422

    # Restoring returns to an earlier manifest as a new snapshot (no uniqueness conflict).
    response = client.post(f"{path}/restore")
    assert response.status_code == 200, response.text
    restored = latest(client, patient_id)
    assert manifest_ids(restored) == manifest_ids(added)
    assert restored["manifest_hash"] == added["manifest_hash"]
    assert restored["sequence"] == removed["sequence"] + 1
    assert client.post(f"{path}/restore").status_code == 409

    # Re-uploading a withdrawn file restores it instead of being ignored as a duplicate.
    client.post(f"{path}/withdraw", json={"reason": "temporary"})
    upload(client, [("c.txt", note("third"))])
    process(app)
    assert target in manifest_ids(latest(client, patient_id))
    listed = {d["id"]: d for d in client.get(f"/api/v1/patients/{patient_id}/documents").json()}
    assert listed[target]["withdrawn"] is False


def test_withdrawal_is_patient_scoped_and_new_patient_gets_own_case(client, app):
    result = upload(
        client,
        [("a.txt", note("first")), ("z.txt", note("other", mrn="P-9", name="Second Patient"))],
    )
    process(app)
    patients = {p["mrn"]: p["id"] for p in client.get("/api/v1/patients").json()}
    assert set(patients) == {"P-1", "P-9"} and len(result["jobs"]) == 2
    other_doc = client.get(f"/api/v1/patients/{patients['P-9']}/documents").json()[0]["id"]
    response = client.post(
        f"/api/v1/patients/{patients['P-1']}/documents/{other_doc}/withdraw",
        json={"reason": "wrong patient"},
    )
    assert response.status_code == 404
    response = client.post(
        f"/api/v1/patients/{patients['P-1']}/documents/{uuid4()}/withdraw",
        json={"reason": "missing"},
    )
    assert response.status_code == 404
    # Withdrawing the only document leaves an empty snapshot, not a stale one.
    only = client.get(f"/api/v1/patients/{patients['P-9']}/documents").json()[0]["id"]
    response = client.post(
        f"/api/v1/patients/{patients['P-9']}/documents/{only}/withdraw", json={"reason": "test"}
    )
    assert response.status_code == 200
    assert latest(client, patients["P-9"])["manifest"] == []
