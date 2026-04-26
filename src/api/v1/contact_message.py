from fastapi import APIRouter, Query
from src.dependencies import AdminDep
from src.models.user import UserRole
from src.schemas.contact_message import ContactMessageIn, ContactMessageOut

from src.core.exceptions import BadRequestException

from src.dependencies import ContactMessageServiceDep

router = APIRouter(prefix="/contact_messages", tags=["Baylanis bo'limi"])

@router.get("/")
async def get_messages(
        admin: AdminDep, 
        service: ContactMessageServiceDep, 
        limit: int | None = Query(None), 
        offset: int | None = Query(None)
    ) -> list[ContactMessageOut]:
    pass
    
@router.get("/{id}")
async def get_one_message(
        id: int,
        admin: AdminDep, 
        service: ContactMessageServiceDep
    ):
    pass
    
@router.post("/")
async def create_message(
        payload: ContactMessageIn,
        service: ContactMessageServiceDep
    ) -> ContactMessageOut:
    pass

@router.patch("/{id}")
async def read_message(
        id: int,
        admin: AdminDep, 
        service: ContactMessageServiceDep
    ):
    pass

@router.delete("/{id}")
async def delete_message(
        id: int,
        admin: AdminDep, 
        service: ContactMessageServiceDep
    ):
    pass