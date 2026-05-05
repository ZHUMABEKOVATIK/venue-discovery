from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.visits import Visit
from .base_repository import BaseRepository


class VisitRepo(BaseRepository[Visit]):
    model = Visit

    async def get_or_create(self, user_id: int, venue_id: int) -> Visit:
        """Возвращает существующий визит или создаёт новый с amount=0"""
        visit = await self.session.scalar(
            select(Visit)
            .options(selectinload(Visit.user))
            .where(Visit.user_id == user_id)
            .where(Visit.venue_id == venue_id)
        )
        if visit is None:
            visit = Visit(user_id=user_id, venue_id=venue_id, amount=0)
            self.session.add(visit)
            await self.session.flush()
            # перезагружаем с user relationship
            await self.session.refresh(visit)
            visit = await self.session.scalar(
                select(Visit)
                .options(selectinload(Visit.user))
                .where(Visit.id == visit.id)
            )
        return visit

    async def get_by_user_and_venue(self, user_id: int, venue_id: int) -> Visit | None:
        return await self.session.scalar(
            select(Visit)
            .where(Visit.user_id == user_id)
            .where(Visit.venue_id == venue_id)
        )