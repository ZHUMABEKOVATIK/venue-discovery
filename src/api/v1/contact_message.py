from fastapi import APIRouter

router = APIRouter(prefix="/contact_messages")

@router.get("/")
async def get_messages(limit: int | None, offset: int | None):
    pass