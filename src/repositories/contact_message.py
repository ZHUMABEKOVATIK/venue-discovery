from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, func
from .base_repository import SoftDeleteRepository

from src.models.contact_message import ContactMessage

class ContactMessageRepo(SoftDeleteRepository[ContactMessage]):
    model = ContactMessage
    
    async def get_all(self, limit: int | None = None, offset: int | None = None, include_deleted: bool = False) -> list[ContactMessage]:
        stmt = (
            select(ContactMessage)
            .limit(limit)
            .offset(offset)
        )

        if not include_deleted:
            stmt = stmt.where(ContactMessage.is_deleted.is_(False))

        return (await self.session.execute(stmt)).scalars().all()

    
    async def read(self, id: int) -> ContactMessage | None:
        try:
            data = (
                await self.session.execute(
                    select(ContactMessage)
                    .where(ContactMessage.id == id)
                    .where(ContactMessage.is_deleted.is_(False))
                    .where(ContactMessage.is_read.is_(False))
                )
            ).scalar_one()
        except NoResultFound:
            return None
        
        data.is_read = True

        await self.session.flush()

        return data