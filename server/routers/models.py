from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Annotated, Literal, Union
from typing_extensions import Self
from uuid import UUID

class LinearLayer(BaseModel):
    layer_type: Literal["Linear"]
    size: int

    @model_validator(mode='after')
    def check_params(self) -> Self:
        assert self.size > 0 and self.size <= 1024, "`size` must be between 1 and 1024, inclusive."
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

class FlattenLayer(BaseModel):
    layer_type: Literal["Flatten"]

class ActivationType(str, Enum):
    relu = "ReLU"
    tanh = "Tanh"

class ActivationLayer(BaseModel):
    layer_type: Literal["Activation"]
    activation: ActivationType

Layer = Annotated[
            Union[LinearLayer, DropoutLayer, Conv2DLayer, FlattenLayer, ActivationLayer],
            Field(discriminator="layer_type")]

class Model(BaseModel):
    name: str
    input_shape: tuple[int, int] # TODO add future flexibility here.. input vector...
    output_shape: int
    layers: list[Layer]


class Model_Out(BaseModel):
    id: UUID
    model: Model
    is_trained: bool

    class Config:
        orm_mode = True


from ..database.database import get_database
from ..database.crud_models import get_all_models, get_model
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/models", tags=["models"])

@router.get("/")
async def get_models(mod_name: str | None = None, db: Session = Depends(get_database)) -> Model_Out | list[Model_Out]:
    if mod_name:
        result = get_model(mod_name, db)
        if result:
            return result
        
        raise HTTPException(status_code=404, detail="Model name not found") 

    return get_all_models(db)


from torch import nn, jit
def construct_pytorch_model(model: Model) -> str:
    pt_layers = []
    current_shape = (model.input_shape[0], model.input_shape[1], 1) # 3rd component is # channels
    for layer in model.layers: 
        if isinstance(layer, FlattenLayer):
            if not isinstance(current_shape, tuple): 
                raise HTTPException(status_code=404, 
                                    detail="Invalid layer sequence: FlattenLayer expects image/array input.") 
            
            pt_layers.append(nn.Flatten())
            current_shape = current_shape[0] * current_shape[1] * current_shape[2] # tuple[int, int, int] -> int

        elif isinstance(layer, LinearLayer):
            if not isinstance(current_shape, int):
                raise HTTPException(status_code=404, 
                                    detail="Invalid layer sequence: LinearLayer expects vector input.") 
            pt_layers.append(nn.Linear(current_shape, layer.size))
            current_shape = layer.size
            
        elif isinstance(layer, Conv2DLayer):
            if isinstance(current_shape, tuple): 
                raise HTTPException(status_code=404, 
                                    detail="Invalid layer sequence: Conv2DLayer expects image/array input.") 
            
            pt_layers.append(nn.Conv2d(current_shape[2], layer.num_channels))
            current_shape = (current_shape[0], current_shape[1], layer.num_channels)

        elif isinstance(layer, DropoutLayer):
            if isinstance(current_shape, int):
                pt_layers.append(nn.Dropout(layer.dropout_prob))
            else: # isinstance(current_shape, tuple)
                pt_layers.append(nn.Dropout2d(layer.dropout_prob))

        elif isinstance(layer, ActivationLayer):
            if layer.activation == ActivationType.relu:
                pt_layers.append(nn.ReLU())
            elif layer.activation == ActivationType.tanh:
                pt_layers.append(nn.Tanh())
        
        else:
            raise HTTPException(status_code=404, 
                                    detail=f"Layer of type {type(layer)} not implemented.") 
    
    # add output layer
    if isinstance(current_shape, int):
        pt_layers.append(nn.Linear(current_shape, model.output_shape))
    else:
        pt_layers.append(nn.Flatten())
        pt_layers.append(nn.Linear(current_shape[0] * current_shape[1] * current_shape[2], 
                                   model.output_shape))
        
    pt_model = nn.Sequential(*pt_layers)
    scripted_module = jit.script(pt_model)
    save_name = f"{model.name}.pt"
    jit.save(scripted_module, save_name)
    return save_name

@router.post("/")
async def create_model(model: Model, db: Session = Depends(get_database)) -> Model:
    # construct pytorch model
    try:
        file_location = construct_pytorch_model(model)
    except Exception as error:
        raise error
    # upload pytorch model to cloud storage

    # return model
    return model




