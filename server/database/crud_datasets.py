from sqlalchemy import Table, select, insert
from sqlalchemy.orm import Session
from .database import DB_Base, engine

class Dataset(DB_Base):
    __table__ = Table('datasets', DB_Base.metadata, autoload_with=engine)

def get_all_datasets(db: Session):
    result = db.execute(
        select(Dataset.name, Dataset.id)
    ).all()

    return result
