from fastapi import APIRouter, HTTPException

from app.db import get_job, insert_job
from app.schemas.job import JobCreate, JobResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobResponse, status_code=201)
def create_job(job: JobCreate):
    new_job_id = insert_job(job.payload)
    return get_job(new_job_id)


@router.get("/{job_id}", response_model=JobResponse)
def read_job(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
