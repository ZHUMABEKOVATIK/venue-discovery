from .base_repository import BaseRepository
from sqlalchemy import select

from src.models.advertising import Advertising

class AdvertisingRepo(BaseRepository[Advertising]):
    model = Advertising

    async def get_all(self) -> list[Advertising]:
        return (await self.session.scalars(
            select(Advertising)
        )).all()