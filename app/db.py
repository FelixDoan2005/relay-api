import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any


def get_connection(path: str | Path = "relay.db") -> sqlite3.Connection:
    return sqlite3.connect(path)


def init_db(path: str | Path = "relay.db") -> None:
    con = get_connection(path)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, status TEXT, payload TEXT)"
    )
    con.commit()
    con.close()


def insert_job(payload: dict[str, Any], path: str | Path = "relay.db") -> str:
    job_id = str(uuid.uuid4())
    con = get_connection(path)
    con.execute(
        "INSERT INTO jobs VALUES (?, ?, ?)", (job_id, "queued", json.dumps(payload))
    )
    con.commit()
    con.close()
    return job_id


def get_job(job_id: str, path: str | Path = "relay.db") -> dict[str, Any] | None:
    con = get_connection(path)
    row = con.execute(
        "SELECT id, status, payload FROM jobs WHERE id = ?", (job_id,)
    ).fetchone()
    con.close()
    if row is None:
        return None
    return {"id": row[0], "status": row[1], "payload": json.loads(row[2])}
