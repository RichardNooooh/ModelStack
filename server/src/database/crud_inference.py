from sqlalchemy import Table, select, insert
from sqlalchemy.orm import Session
from .database import Model
from uuid import UUID

def get_model_path(mod_id: UUID, db: Session):
    result = db.execute(
        select(Model.file_path) # TODO add warning if model isn't trained yet...
        .where(Model.id == mod_id)
    ).first()

    print(result)

    return result[0]
