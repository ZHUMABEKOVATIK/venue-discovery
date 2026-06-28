from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Generic
from sqlalchemy import select, func
from src.db.base import IDMixIn, SoftDeleteMixIn

T = TypeVar("T", bound=IDMixIn)
SDT = TypeVar("SDT", bound=SoftDeleteMixIn)

class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        return obj
    
    async def update(self, id: int, **kwargs) -> T | None:
        data = (
            await self.session.execute(
                select(self.model)
                .where(self.model.id == id)
            )
        ).scalar_one_or_none()

        if data is None:
            return None

        for key, value in kwargs.items():
            if hasattr(data, key):
                setattr(data, key, value)
        
        await self.session.flush()
        return data
    
    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.flush()
    
    async def get_by_id(self, id: int) -> T | None:
        return await self.session.scalar(
            select(self.model).where(self.model.id == id)
        )
    
    async def get_total(self) -> int:
        return await self.session.scalar(
            select(func.count(self.model.id))
        )
    
class SoftDeleteRepository(BaseRepository[SDT]):
    async def update(self, id: int, **kwargs) -> SDT | None:
        data = (
            await self.session.execute(
                select(self.model)
                .where(self.model.id == id)
                .where(self.model.is_deleted.is_(False))
            )
        ).scalar_one_or_none()

        if data is None:
            return None

        for key, value in kwargs.items():
            if hasattr(data, key):
                setattr(data, key, value)
        
        await self.session.flush()
        return data

    async def delete(self, obj: SDT) -> None:
        obj.is_deleted = True
        await self.session.flush()

    async def get_by_id(self, id: int) -> SDT | None:
        return await self.session.scalar(
            select(self.model)
            .where(self.model.id == id)
            .where(self.model.is_deleted.is_(False))
        )

    async def get_total(self) -> int:
        return await self.session.scalar(
            select(func.count(self.model.id))
            .where(self.model.is_deleted.is_(False))
        )