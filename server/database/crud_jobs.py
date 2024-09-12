from sqlalchemy import Table, select, insert
from sqlalchemy.orm import Session
from .database import DB_Base, engine, Job, Model

from fastapi import HTTPException

import requests

def get_all_datasets(k: int, db: Session):
    result = db.execute(
        select(Job.id, Job.model_id, Job.dataset_name, 
               Job.job_status, Job.start_time, Job.parameters).
        limit(k)
    ).all()

    return result

def create_job(job_req: dict, db: Session):
    result = db.execute(
        insert(Job).values(model_id=job_req["model_id"],
                           dataset_name=job_req["dataset_name"],
                           parameters={"learning_rate":job_req["parameters"].learning_rate,
                                       "num_epochs":job_req["parameters"].num_epochs}).
        returning(Job.id, Job.model_id, Job.dataset_name, Job.job_status, Job.start_time, Job.parameters)
    ).first()
    job_id = result[0]
    model_path = db.execute(
        select(Model.file_path).where(Model.id == job_req["model_id"])
    ).first()
    if not model_path:
        raise HTTPException(status_code=404, detail="invalid model id")
    model_path = model_path[0]
    print(f"Found model path for job: {model_path}")

    compute_requestbody = {"job_id": str(job_id),
                           "model_path": str(model_path),
                           "dataset": job_req["dataset_name"],
                           "parameters": dict(job_req["parameters"])}
    print(compute_requestbody)
    compute_req = requests.post("http://localhost:42069/", json=compute_requestbody)
    if compute_req.status_code != 200:
        raise HTTPException(status_code=404)
    print(compute_req.text)
    db.commit()
    return result
