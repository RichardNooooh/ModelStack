from sqlalchemy import Table, select, insert
from sqlalchemy.orm import Session
from .database import DB_Base, engine, Dataset

def get_all_datasets(db: Session):
    result = db.execute(
        select(Dataset.name, Dataset.id)
    ).all()

    return result
