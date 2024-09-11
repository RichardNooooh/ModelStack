from .schemas import *
from fastapi import FastAPI
from uuid import UUID

fake_database = {"test": {
    "owner": "asdfasdfasd_id",
    "name": "test_model",
    "layers": [
        {
            "type": "linear",
            "size": 10,
        },
        {
            "type": "linear",
            "size": 5,
        }
    ]
}}
app = FastAPI()

@app.get("/models/")
async def get_model(model_id: UUID | str | None = None) -> Model:
    return fake_database[model_id]

@app.post("/models/", response_model=Model)
async def create_model(model: Model) -> Model:
    # construct_torch_model(model)
    return model
