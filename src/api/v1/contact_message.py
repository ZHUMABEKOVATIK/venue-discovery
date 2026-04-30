from fastapi import APIRouter, Query
from src.dependencies import AdminDep
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
    return await service.get_all(limit=limit, offset=offset)
    
@router.get("/{id}")
async def get_one_message(
        id: int,
        admin: AdminDep, 
        service: ContactMessageServiceDep
    ):
    return await service.get_by_id(id)
    
@router.post("/")
async def create_message(
        payload: ContactMessageIn,
        service: ContactMessageServiceDep
    ) -> ContactMessageOut:
    return await service.create(payload)

@router.patch("/read/{id}", description="Xabar oqildi dep qaldiriw")
async def read_message(
        id: int,
        admin: AdminDep, 
        service: ContactMessageServiceDep
    ):
    return await service.read(id)

@router.delete("/{id}")
async def delete_message(
        id: int,
        admin: AdminDep, 
        service: ContactMessageServiceDep
    ):
    await service.delete(id)