from .schemas import LayerType, Layer, Model
from fastapi import FastAPI

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

@app.get("/models/{model_id}")
async def get_model(model_id: str) -> Model:
    return fake_database[model_id]
