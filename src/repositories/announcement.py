from .base_repository import SoftDeleteRepository
from sqlalchemy import select

from src.models.announcement import Announcement
from src.models.model_enums import DataStatus

class AnnouncementRepo(SoftDeleteRepository[Announcement]):
    model = Announcement

    async def get_all(
        self,
        *,
        user_id: int | None = None,
        only_approved: bool = False,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[Announcement]:
        stmt = (
            select(Announcement)
            .where(Announcement.is_deleted.is_(False))
            .order_by(Announcement.id.desc())
        )

        if only_approved:
            stmt = stmt.where(Announcement.status == DataStatus.approved)

        if user_id is not None:
            stmt = stmt.where(Announcement.user_id == user_id)

        stmt = stmt.offset(offset).limit(limit)
        return (await self.session.scalars(stmt)).all()