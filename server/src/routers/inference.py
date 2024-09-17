# Method 4 from https://stackoverflow.com/a/70640522/19918922
from fastapi import APIRouter, File, Body, UploadFile, Depends
from pydantic import BaseModel, model_validator
from typing import Optional
from uuid import UUID
import json

from ..database.database import get_database
from ..database.crud_inference import get_model_path
from sqlalchemy.orm import Session

import torch
from torch import jit
from torchvision.transforms.functional import pil_to_tensor

import io

from PIL import Image
import numpy as np

class InferenceRequest(BaseModel):
    mod_id: UUID

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class InferenceResult(BaseModel):
    file_name: str
    classification: int
    probability: float

class InferenceResponse(BaseModel):
    mod_id: UUID
    results: list[InferenceResult]


router = APIRouter(prefix="/inference", tags=["inference"])

CACHED_MODEL = ("fake_id", "fake_path")

@router.post("/")
async def get_predictions(data: InferenceRequest = Body(...), files: list[UploadFile] = File(...), db: Session = Depends(get_database)) -> InferenceResponse:
    global CACHED_MODEL

    model_path = None
    if data.mod_id == CACHED_MODEL[0]:
        model_path = CACHED_MODEL[1]
    else:
        model_path = get_model_path(data.mod_id, db)
        CACHED_MODEL = (data.mod_id, model_path)

    model = jit.load(model_path)
    model.eval()

    outputs = []
    for file in files:
        # obtain img data
        request_object_content = await file.read()

        # convert to image data type
        # TODO wrap this in try-catch error
        # TODO make this more efficient by putting all images into a single tensor along batch dimension?
        im = Image.open(io.BytesIO(request_object_content)).convert("L")
        im.thumbnail((28, 28), Image.Resampling.LANCZOS)
        np_im = np.array(im, dtype=np.float32)
        np_im /= 255.0
        input_im = torch.from_numpy(np_im)
        input_im = input_im[None, :, :] # add a batch dimension

        # calculate prediction
        output = model(input_im)
        probabilities = torch.softmax(output, dim=1)
        predicted_prob, predicted_class = torch.max(probabilities, dim=1)
        outputs.append({"file_name": file.filename,
                        "classification": int(predicted_class.item()),
                        "probability": predicted_prob.item()})


    return {"mod_id": data.mod_id, "results": outputs}
