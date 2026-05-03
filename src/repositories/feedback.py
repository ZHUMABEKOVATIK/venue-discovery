from .base_repository import BaseRepository
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.feedback import Feedback

class FeedbackRepo(BaseRepository[Feedback]):
    model = Feedback

    async def get_all(self, *, venue_id: int | None = None, offset: int | None = None, limit: int | None = None) -> list[Feedback]:
        stmt = (
            select(Feedback)
            .options(selectinload(Feedback.user))
            .order_by(Feedback.id.desc())
        )
        if venue_id is not None:
            stmt = stmt.where(Feedback.venue_id == venue_id)

        stmt = stmt.offset(offset).limit(limit)

        return (await self.session.scalars(stmt)).all()