import os
from uuid import uuid4

import pytest
from clinical.api.main import create_app
from clinical.infrastructure.config import Settings
from fastapi.testclient import TestClient


@pytest.fixture
def app(tmp_path):
    url = os.environ.get("EHR_TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set EHR_TEST_DATABASE_URL to the migrated isolated PostgreSQL database")
    assert url.rsplit("/", 1)[-1] == "ehr_test", "Integration tests require ehr_test database"
    return create_app(
        Settings(
            database_url=url,
            object_root=tmp_path / "objects",
            environment="test",
            browser_origin="http://testserver",
            dev_tenant=uuid4(),
            dev_actor=uuid4(),
            session_secret="integration-test-secret-never-used-in-production",
            anthropic_api_key="",
        )
    )


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        response = client.post("/api/v1/dev-session", headers={"Origin": "http://testserver"})
        assert response.status_code == 200
        client.headers.update(
            {"Origin": "http://testserver", "X-CSRF-Token": response.json()["csrf_token"]}
        )
        yield client
