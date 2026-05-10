from fastapi import APIRouter, Query, status
from src.dependencies import AdminDep
from src.schemas.contact_message import ContactMessageIn, ContactMessageOut

from src.dependencies import ContactMessageServiceDep

router = APIRouter(prefix="/contact_messages", tags=["Contact Us"])

@router.get("/", response_model=list[ContactMessageOut])
async def get_messages(
        admin: AdminDep, 
        service: ContactMessageServiceDep, 
        limit: int | None = Query(None), 
        offset: int | None = Query(None)
    ):
    return await service.get_all(limit=limit, offset=offset)
    
@router.get("/{id}", response_model=ContactMessageOut)
async def get_one_message(
        id: int,
        admin: AdminDep, 
        service: ContactMessageServiceDep
    ):
    return await service.get_by_id(id)
    
@router.post("/", response_model=ContactMessageOut, status_code=status.HTTP_201_CREATED)
async def create_message(
        payload: ContactMessageIn,
        service: ContactMessageServiceDep
    ):
    return await service.create(payload)

@router.patch("/read/{id}", description="Xabar oqildi dep qaldiriw", response_model=ContactMessageOut)
async def read_message(
        id: int,
        admin: AdminDep, 
        service: ContactMessageServiceDep
    ):
    return await service.read(id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
        id: int,
        admin: AdminDep, 
        service: ContactMessageServiceDep
    ):
    await service.delete(id)