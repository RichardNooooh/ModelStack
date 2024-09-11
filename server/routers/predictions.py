from fastapi import APIRouter()
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()

class BasePrediction(BaseModel):
    model_id: UUID

class Prediction_In(BasePrediction):
    input_data: 


@router.post("/predictions/", tags=["predictions"])
async def load_prediction() -> list[str]:
    if not model_name:
        # SQL: SELECT name FROM datasets
        return None # read list of names
