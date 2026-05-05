from .base_repository import SoftDeleteRepository
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.announcement import Announcement
from src.models.model_enums import DataStatus

class AnnouncementRepo(SoftDeleteRepository[Announcement]):
    model = Announcement

    async def get_by_id(self, id: int) -> Announcement | None:
        return await self.session.scalar(
            select(self.model)
            .where(self.model.id == id)
            .options(selectinload(self.model.user))
            .where(self.model.is_deleted.is_(False))
        )

    async def get_all(
        self,
        *,
        user_id: int | None = None,
        only_approved: bool = False,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[Announcement]:
        stmt = (
            select(self.model)
            .where(self.model.is_deleted.is_(False))
            .options(selectinload(self.model.user))
            .order_by(self.model.id.desc())
        )

        if only_approved:
            stmt = stmt.where(self.model.status == DataStatus.approved)

        if user_id is not None:
            stmt = stmt.where(self.model.user_id == user_id)

        stmt = stmt.offset(offset).limit(limit)
        return (await self.session.scalars(stmt)).all()