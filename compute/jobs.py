from .database import SessionLocal, DB_Job
from sqlalchemy import update

from uuid import UUID
from collections import deque
from enum import Enum

from multiprocessing import Lock

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    CANCELLED = "cancelled"
    DONE = "done"
    ERROR = "error" # unused

class Job:
    db = SessionLocal()

    def __init__(self, id: UUID):
        self.id = id
        self.status = JobStatus.PENDING

    def updateStatus(self, new_status: JobStatus):
        self.status = new_status

        Job.db.execute(
            update(DB_Job).
            where(DB_Job.job_id == self.id).
            values(job_status=new_status)
        )
        Job.db.commit()
    
class JobQueue:
    queue = deque()
    lock = Lock()

