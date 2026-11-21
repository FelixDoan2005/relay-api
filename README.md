# Relay

A job-processing REST API. Clients submit slow tasks (jobs); the API stores the job and immediately replies with status `queued`. Separate worker processes pick jobs up, run them, and update their status. Clients poll via `GET` or receive a webhook when the job finishes.

The focus is API and backend design, especially reliability features, not the job logic itself.

## Architecture

```
Client --> API (FastAPI) --> Queue/Storage --> Workers
   ^            |                                  |
   |            v                                  v
   +------ GET /v1/jobs/{id}              run job, update status
   +------ webhook on completion <-----------------+
```

Job lifecycle: `queued -> running -> done | failed`

## Planned features

- [ ] API key authentication and per-key permissions
- [ ] Versioned endpoints (`/v1/...`), pagination, filtering, consistent error format
- [ ] Per-key rate limiting (Redis)
- [ ] Idempotency keys (retried requests don't create duplicate jobs)
- [ ] Workers with retries, exponential backoff and a dead-letter queue
- [ ] Webhooks on job completion
- [ ] SQLite first, then Postgres + Redis via Docker Compose
- [ ] Tests including failure cases
- [ ] GitHub Actions CI
- [ ] Load testing

## Setup

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```
uvicorn app.main:app --reload
pytest
```
