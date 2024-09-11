from fastapi import APIRouter()
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Annotated, Literal, Union
from typing_extensions import Self
from uuid import UUID

import torch.nn as nn

class ActivationType(str, Enum):
    relu = "ReLU"
    tanh = "Tanh"

class BaseLayer(BaseModel):
    activation: ActivationType | None = None


class LinearLayer(BaseLayer):
    layer_type: Literal["Linear"]
    size: int

    @model_validator(mode='after')
    def check_params(self) -> Self:
        assert self.size > 0 and self.size <= 1024, "`size` must be between 1 and 1024, inclusive."
        return self

class DropoutLayer(BaseLayer):
    layer_type: Literal["Dropout"]
    dropout_prob: float = 0.5

    @model_validator(mode='after')
    def check_params(self) -> Self:
        assert self.dropout_prob >= 0.0 and self.dropout_prob <= 1.0, \
        "`dropout_prob` must be between 0.0 and 1.0, inclusive."
        # assert (
        #     self.type == LayerType.dropout1d 
        #     or self.type == LayerType.dropout2d
        #     ), "`dropout_prob` should only be used for DropoutLayers"
        return self

class Conv2DLayer(BaseLayer):
    layer_type: Literal["Conv2d"]
    num_channels: int
    kernel: int | None = 3

    @model_validator(mode='after')
    def check_params(self) -> Self:
        assert self.num_channels > 0 and self.num_channels < 256, \
                "`num_channels` must be in the interval [1, 255]"
        assert self.kernel > 0 and self.kernel < 4, \
                "`kernel` must be in [1, 3]"
        return self

class Flatten(BaseLayer):
    layer_type: Literal["Flatten"]

Layer = Annotated[
            Union[LinearLayer, DropoutLayer, Conv2DLayer, Flatten],
            Field(discriminator="layer_type")]

class Model(BaseModel):
    name: str
    input_shape: tuple[int, int] # TODO add future flexibility here.. input vector...
    output_shape: int
    layers: list[Layer]

class Model_Out(Model):
    uuid: UUID | None = None


router = APIRouter()

@router.get("/models/", tags=["models"])
async def get_models(model_name: str | None = None) -> list[str] | Model_Out:
    if not model_name:
        # SQL: SELECT model_name FROM models
        return None # read list of names

@router.post("/models/", tags=["models"])
async def create_model(model: Model) -> Model_Out:
    # construct pytorch model

    # upload pytorch model to cloud storage

    # return model
    return None




