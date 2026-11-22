import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # relay.db is a relative path, so running from a temp folder keeps the
    # real database untouched
    monkeypatch.chdir(tmp_path)
    # "with" runs the lifespan, which creates the jobs table
    with TestClient(app) as client:
        yield client


def test_create_and_get_job(client) -> None:
    payload = {"url": "https://example.com"}

    response = client.post("/v1/jobs", json={"payload": payload})
    assert response.status_code == 201
    job = response.json()
    assert job["status"] == "queued"
    assert job["payload"] == payload

    response = client.get(f"/v1/jobs/{job['id']}")
    assert response.status_code == 200
    assert response.json() == job


def test_get_unknown_job_returns_404(client) -> None:
    response = client.get("/v1/jobs/doesnt-exist")
    assert response.status_code == 404


def test_create_job_without_payload_returns_422(client) -> None:
    response = client.post("/v1/jobs", json={})
    assert response.status_code == 422
