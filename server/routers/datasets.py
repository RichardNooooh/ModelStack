from fastapi import APIRouter

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.get("/")
async def get_datasets() -> list[str]:
    pass
    if not mod_name:
        # SQL: SELECT name FROM datasets
        return None # read list of names
