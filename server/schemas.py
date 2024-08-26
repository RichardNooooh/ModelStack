# from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

class LayerType(str, Enum):
    linear = "linear"
    conv2d = "convolutional_2d"
    dropout2d = "dropout_2d"
    batchnorm2d = "batch_norm_2d"
    relu = "activation_ReLU"
    tanh = "activation_tanh"

class Layer(BaseModel):
    type: LayerType
    size: int | None = None
    kernel: int | None = None

class Model(BaseModel):
    owner: str      # user id
    name: str
    layers: list[Layer]
