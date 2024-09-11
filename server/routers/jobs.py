from fastapi import APIRouter()
from pydantic import BaseModel
from enum import Enum
from uuid import UUID
router = APIRouter()


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    cancelled = "cancelled"
    done = "done"
    error = "error"

class Job(BaseModel):
    job_id: UUID
    model_name: str
    dataset_name: str
    job_status: JobStatus
    start_time: str

class JobRequest(BaseModel):
    model_id: UUID
    dataset_name: str


@router.get("/jobs/", tags=["jobs"])
async def get_jobs(num: int = 5) -> list[Job]:
    return None # read list of names

@router.post("/jobs/", tags=["jobs"])
async def start_job(job_req: JobRequest) -> Job:
    return None # socket

@router.get("/jobs/{job_id}", tags=["jobs"])
async def get_job(job_id: UUID) -> Job:
    return None

@router.post("/jobs/{job_id}", tags=["jobs"])
async def cancel_job(job_id: UUID) -> Job:
    return None # socket

