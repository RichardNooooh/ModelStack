from fastapi import APIRouter, Depends
from pydantic import BaseModel
from enum import Enum
from uuid import UUID

from ..database.crud_jobs import get_all_datasets, create_job
from ..database.database import get_database
from sqlalchemy.orm import Session

import datetime

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
    id: UUID
    model_id: UUID
    dataset_name: str
    job_status: JobStatus
    start_time: datetime.datetime
    parameters: JobParameters

class JobRequest(BaseModel):
    model_id: UUID
    dataset_name: str
    parameters: JobParameters



router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/")
async def get_jobs(num: int = 5, db: Session = Depends(get_database)) -> list[Job]:
    return get_all_datasets(num, db)

@router.post("/")
async def create_and_start_job(job_req: JobRequest, db: Session = Depends(get_database)) -> Job:
    return create_job(dict(job_req), db)

# @router.get("/{job_id}")
# async def get_job(job_id: UUID) -> Job:
#     return None

# @router.post("/{job_id}")
# async def cancel_job(job_id: UUID) -> Job:
#     return None # socket

