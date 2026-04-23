from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_exists(self, email: str) -> bool:
        stmt = select(User.id).where(User.email == email)

        data = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()
        return data is not None

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_one(self, *, _id: int | None = None, email: str | None = None) -> User | None:
        if not any([_id, email]):
            raise ValueError("At least one parameter is required")
        
        stmt = select(User)

        if _id is not None:
            stmt = stmt.where(User.id == _id)
        if email is not None:
            stmt = stmt.where(User.email == email)

        data = (
            await self.session.execute(stmt.where(User.is_deleted.is_(False)))
        ).scalar_one_or_none()
        
        return data
    
    async def delete(self, _id: int) -> bool:
        stmt = select(User).where(User.id == _id)

        data = (
            await self.session.execute(stmt.where(User.is_deleted.is_(False)))
        ).scalar_one_or_none()

        if data is None:
            return False
        
        data.email = None
        data.is_deleted = True

        await self.session.flush()
        return True