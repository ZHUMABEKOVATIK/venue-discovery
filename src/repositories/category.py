from .base_repository import BaseRepository
from sqlalchemy import select

from src.models.category import Category

class CategoryRepo(BaseRepository[Category]):
    model = Category

    async def get_all(self) -> list[Category]:
        return (
            await self.session.execute(
                select(Category).where(Category.parent_id.is_(None))
            )
        ).scalars().all()
    

class SubCategoryRepo(BaseRepository[Category]):
    model = Category

    async def parent_exists(self, id: int) -> bool:
        data = (
            await self.session.execute(
                select(Category)
                .where(Category.id == id)
                .where(Category.parent_id.is_(None))
            )
        ).scalar_one_or_none()
        return data is not None
    
    async def get_all(self, parent_id: int) -> list[Category]:
        return (
            await self.session.execute(
                select(Category).where(Category.parent_id == parent_id)
            )
        ).scalars().all()
    
    async def get_by_id(self, id: int) -> Category | None:
        return await self.session.scalar(
            select(Category)
            .where(Category.id == id)
            .where(Category.parent_id.is_not(None))
        )