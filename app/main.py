from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.jobs import router as jobs_router
from app.db import init_db


@asynccontextmanager
async def startup(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Relay", version="0.1.0", lifespan=startup)
app.include_router(jobs_router, prefix="/v1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
