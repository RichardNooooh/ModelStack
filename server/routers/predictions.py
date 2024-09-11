# Method 4 from https://stackoverflow.com/a/70640522/19918922
from fastapi import AppRouter, File, Body, UploadFile
from pydantic import BaseModel, model_validator
from typing import Optional
from uuid import UUID
import json

class PredictionRequest(BaseModel):
    model_id: UUID

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class PredictionResult(BaseModel):
    classification: int
    probability: float

class PredictionResponse(BaseModel):
    model_id: UUID
    results: list[PredictionResponse]

router = APIRouter()

@router.post("/predictions/")
async def load_predictions(data: PredictionRequest = Body(...), files: list[UploadFile] = File(...)) -> PredictionResponse:
    return {"JSON Payload": data, "Filenames": [file.filename for file in files]}
