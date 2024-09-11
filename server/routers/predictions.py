# Method 4 from https://stackoverflow.com/a/70640522/19918922
from fastapi import APIRouter, File, Body, UploadFile
from pydantic import BaseModel, model_validator
from typing import Optional
from uuid import UUID
import json

class PredictionRequest(BaseModel):
    mod_id: UUID

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
    mod_id: UUID
    results: list[PredictionResult]



router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/")
async def load_predictions(data: PredictionRequest = Body(...), files: list[UploadFile] = File(...)) -> PredictionResponse:
    return {"JSON Payload": data, "Filenames": [file.filename for file in files]}
