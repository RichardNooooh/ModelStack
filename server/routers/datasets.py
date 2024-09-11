from fastapi import APIRouter()

router = APIRouter()

@router.get("/datasets/", tags=["datasets"])
async def get_datasets() -> list[str]:
    if not model_name:
        # SQL: SELECT name FROM datasets
        return None # read list of names
