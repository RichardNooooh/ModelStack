from fastapi import APIRouter
from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    cancelled = "cancelled"
    done = "done"
    error = "error"

class JobParameters(BaseModel):
    learning_rate: float
    num_epochs: int

class Job(BaseModel):
    job_id: UUID
    mod_name: str
    dataset_name: str
    job_status: JobStatus
    start_time: str
    parameters: JobParameters

class JobRequest(BaseModel):
    mod_name: UUID
    dataset_name: str
    parameters: JobParameters



router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/")
async def get_jobs(num: int = 5) -> list[Job]:
    return None # read list of names

@router.post("/")
async def start_job(job_req: JobRequest) -> Job:
    return None # socket

@router.get("/{job_id}")
async def get_job(job_id: UUID) -> Job:
    return None

@router.post("/{job_id}")
async def cancel_job(job_id: UUID) -> Job:
    return None # socket

