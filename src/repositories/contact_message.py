from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, func

from src.models.contact_message import ContactMessage

class ContactMessageRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, msg: ContactMessage) -> ContactMessage:
        self.session.add(msg)
        await self.session.flush()
        return msg
    
    async def get_all(self, limit: int | None = None, offset: int | None = None, include_deleted: bool = False) -> list[ContactMessage]:
        stmt = (
            select(ContactMessage)
            .limit(limit)
            .offset(offset)
        )

        if not include_deleted:
            stmt = stmt.where(ContactMessage.is_deleted.is_(False))

        return (await self.session.execute(stmt)).scalars().all()
    
    async def get_one(self, id: int) -> ContactMessage | None:
        return await self.session.scalar(
            select(ContactMessage).where(ContactMessage.id == id).where(ContactMessage.is_deleted.is_(False))
        )
    
    async def get_total(self) -> int:
        return await self.session.scalar(
            select(func.count(ContactMessage.id))
            .where(ContactMessage.is_deleted.is_(False))
        )
    
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
    
    async def delete(self, id: int) -> bool:
        try:
            data = (
                await self.session.execute(
                    select(ContactMessage)
                    .where(ContactMessage.id == id)
                )
            ).scalar_one()
        except NoResultFound:
            return False
        
        data.is_deleted = True

        await self.session.flush()

        return True