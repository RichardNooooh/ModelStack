from sqlalchemy import Table, select, insert
from sqlalchemy.orm import Session

from .database import DB_Base, engine

class Model(DB_Base):
    __table__ = Table('models', DB_Base.metadata, autoload_with=engine)

def get_all_models(db: Session):
    result = db.execute(
        select(Model.id, Model.is_trained, Model.model)
    ).all()

    return result

def get_model(model_name: str, db: Session):
    result = db.execute(
        select(Model.id, Model.is_trained, Model.model)
        .where(Model.model["name"].astext == model_name)
    ).first()

    return result
    

