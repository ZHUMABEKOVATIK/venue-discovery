from src.repositories.contact_message import ContactMessageRepo
from src.models.contact_message import ContactMessage
from src.core import NotFoundException
from src.schemas.contact_message import ContactMessageIn


class ContactMessageService:
    def __init__(self, repo: ContactMessageRepo):
        self.repo = repo

    async def create(self, payload: ContactMessageIn) -> ContactMessage:
        msg = ContactMessage(
            email=payload.email,
            name=payload.name,
            message=payload.message
        )
        data = await self.repo.create(msg)
        return data

    async def get_by_id(self, id: int) -> ContactMessage:
        data = await self.repo.get_by_id(id)
        if data is None:
            raise NotFoundException("Message not found")
        return data
    
    async def get_all(self, limit: int | None = None, offset: int | None = None, include_deleted: bool = False) -> list[ContactMessage]:
        data = await self.repo.get_all(limit=limit, offset=offset, include_deleted=include_deleted)
        return data
    
    async def read(self, id: int) -> ContactMessage:
        data = await self.repo.read(id)
        if data is None:
            raise NotFoundException("Message not found")
        return data
    
    async def delete(self, id: int) -> None:
        data = await self.repo.get_by_id(id)
        if data is None:
            raise NotFoundException("Message not found")
        await self.repo.delete(data)