import json
import sqlite3

from app.db import get_job, init_db, insert_job, list_jobs


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


def test_list_jobs_returns_empty_list_when_no_jobs(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)

    assert list_jobs(path=db_path) == []


def test_list_jobs_returns_all_jobs_in_insertion_order(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    ids = [insert_job({"n": i}, db_path) for i in range(3)]

    jobs = list_jobs(path=db_path)

    assert [job["id"] for job in jobs] == ids


def test_list_jobs_limit_caps_the_number_returned(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    for i in range(5):
        insert_job({"n": i}, db_path)

    jobs = list_jobs(limit=2, path=db_path)

    assert len(jobs) == 2


def test_list_jobs_offset_skips_the_first_jobs(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    ids = [insert_job({"n": i}, db_path) for i in range(5)]

    jobs = list_jobs(limit=2, offset=3, path=db_path)

    assert [job["id"] for job in jobs] == ids[3:5]
