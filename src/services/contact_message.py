from src.repositories.contact_message import ContactMessageRepo
from src.models.contact_message import ContactMessage
from src.core.exceptions import NotFoundException
from src.schemas.contact_message import ContactMessageIn, ContactMessageOut


class ContactMessageService:
    def __init__(self, repo: ContactMessageRepo):
        self.repo = repo

    async def create(self, payload: ContactMessageIn) -> ContactMessage:
        msg = ContactMessage(
            email=payload.email,
            name=payload.name,
            message=payload.message
        )
        data = self.repo.create(msg)
        return data

    async def get_by_id(self, id: int) -> ContactMessage:
        data = await self.repo.get_one(id)
        if data is None:
            raise NotFoundException("Message not found!")
        return data
    
    async def get_all(self) -> list[ContactMessage]:
        data = await self.repo.get_all()
        return data
    
    async def read(self, id: int) -> ContactMessage:
        data = await self.repo.read(id)
        if data is None:
            raise NotFoundException("Message not found!")
        return data
    
    async def delete(self, id: int) -> bool:
        data = await self.repo.delete(id)
        return data