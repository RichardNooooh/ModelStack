from database import SessionLocal, DB_Job
from sqlalchemy import update

from uuid import UUID
from collections import deque
from enum import Enum
import json

from threading import Lock

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    CANCELLED = "cancelled"
    DONE = "done"
    ERROR = "error" # unused

class Job:
    def __init__(self, id: UUID):
        self.id = id
        self.status = JobStatus.PENDING
        self.db = SessionLocal()

    def updateStatus(self, new_status: JobStatus):
        self.status = new_status

        Job.db.execute(
            update(DB_Job).
            where(DB_Job.job_id == self.id).
            values(job_status=new_status)
        )
        Job.db.commit()

class JobEncoder(json.JSONEncoder):
    def default(self, obj):
        return {"id": obj.id, "status": obj.self.status}
    
class JobQueue:
    queue = deque()
    lock = Lock()

