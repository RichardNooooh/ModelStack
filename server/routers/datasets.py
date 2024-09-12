from fastapi import APIRouter, Depends
from ..database.database import get_database
from ..database.crud_datasets import get_all_datasets
from sqlalchemy.orm import Session

from pydantic import BaseModel
from uuid import UUID
class Dataset(BaseModel):
    name: str
    id: UUID

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.get("/")
async def get_available_datasets(db: Session = Depends(get_database)) -> list[Dataset]:
    return get_all_datasets(db)
