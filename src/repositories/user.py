from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_exists(self, email: str) -> bool:
        data = await self.session.scalar(
            select(User.id).where(User.email == email)
        )
        return data is not None

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_one(self, *, _id: int | None = None, email: str | None = None) -> User | None:
        if not any([_id, email]):
            raise ValueError("At least one parameter is required")

        stmt = select(User).where(User.is_deleted.is_(False))

        if _id is not None:
            stmt = stmt.where(User.id == _id)
        if email is not None:
            stmt = stmt.where(User.email == email)

        return await self.session.scalar(stmt)

    async def update(self, _id: int, **kwargs) -> User | None:
        user = await self.get_one(_id=_id)
        if user is None:
            return None

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        await self.session.flush()
        return user

    async def delete(self, _id: int) -> bool:
        user = await self.get_one(_id=_id)
        if user is None:
            return False

        user.email = None
        user.is_deleted = True
        await self.session.flush()
        return True
