from typing import Any

from pydantic import BaseModel


class JobCreate(BaseModel):
    payload: dict[str, Any]


class JobResponse(BaseModel):
    id: str
    status: str
    payload: dict[str, Any]
