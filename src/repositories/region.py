from .base_repository import BaseRepository
from sqlalchemy import select

from src.models.region import Region

class RegionRepo(BaseRepository[Region]):
    model = Region

    async def get_all(self) -> list[Region]:
        return (
            await self.session.execute(
                select(Region)
            )
        ).scalars().all()