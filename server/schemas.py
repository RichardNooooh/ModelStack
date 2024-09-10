# from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Annotated, Literal, Union
from typing_extensions import Self

class LinearLayer(BaseModel):
    layer_type: Literal["Linear"]
    size: int

    @model_validator(mode='after')
    def check_params(self) -> Self:
        assert self.size > 0 and self.size < 256, "`size` must be between 1 and 255, inclusive."
        # assert self.type == LayerType.linear, "`size` should only be used for LinearLayers"
        return self


class DropoutLayer(BaseModel):
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

class Conv2DLayer(BaseModel):
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

Layer = Annotated[
            Union[LinearLayer, DropoutLayer, Conv2DLayer],
            Field(discriminator="layer_type")]

class Model(BaseModel):
    name: str
    layers: list[Layer]
