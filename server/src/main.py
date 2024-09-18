from fastapi import FastAPI
from .routers import datasets
from .routers import jobs
from .routers import models
from .routers import inference

app = FastAPI()
app.include_router(datasets.router)
app.include_router(jobs.router)
app.include_router(models.router)
app.include_router(inference.router)
