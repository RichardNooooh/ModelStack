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
    def __init__(self, id: UUID, model_path: str, 
                 lr: float, epochs: int, 
                 data_path: str = "../storage/"):
        self.id = id
        self.model_path = model_path
        self.data_path = data_path
        
        self.lr = lr
        self.num_epochs = epochs

        self.status = JobStatus.PENDING
        self.db = SessionLocal()

    def updateStatus(self, new_status: JobStatus):
        self.status = new_status

        self.db.execute(
            update(DB_Job).
            where(DB_Job.id == self.id).
            values(job_status=new_status)
        )
        self.db.commit()

class JobEncoder(json.JSONEncoder):
    def default(self, obj):
        return {"id": obj.id, "status": obj.self.status}
    
class JobQueue:
    queue = deque()
    lock = Lock()

