import json
import sqlite3

from app.db import get_job, init_db, insert_job


def test_init_db_creates_jobs_table(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)

    con = sqlite3.connect(db_path)
    tables = [row[0] for row in con.execute("SELECT name FROM sqlite_master")]
    con.close()

    assert "jobs" in tables


def test_insert_job_saves_queued_job(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    payload = {"url": "https://example.com"}
    job_id = insert_job(payload, db_path)

    con = sqlite3.connect(db_path)
    row = con.execute(
        "SELECT status, payload FROM jobs WHERE id = ?", (job_id,)
    ).fetchone()
    con.close()
    status, saved_payload = row
    assert status == "queued"
    assert json.loads(saved_payload) == payload


def test_get_job_returns_inserted_job(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    payload = {"url": "https://example.com"}
    job_id = insert_job(payload, db_path)
    job = get_job(job_id, db_path)
    assert job["id"] == job_id
    assert job["status"] == "queued"
    assert job["payload"] == payload


def test_get_job_returns_none_for_unknown_id(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    assert get_job("doesnt-exist", db_path) is None
