from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.venue import Venue
from src.models.model_enums import DataStatus
from .base_repository import BaseRepository


class VenueRepo(BaseRepository[Venue]):
    model = Venue

    async def get_all(
        self,
        *,
        owner_id: int | None = None,
        status: DataStatus | None = None,
        category_id: int | None = None,
        subcategory_id: int | None = None,
        region_id: int | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[Venue]:
        stmt = (
            select(Venue)
            .options(
                selectinload(Venue.owner),
                selectinload(Venue.region),
                selectinload(Venue.category),
                selectinload(Venue.subcategory),
            )
            .where(Venue.is_deleted.is_(False))
            .order_by(Venue.id.desc())
        )

        if owner_id is not None:
            stmt = stmt.where(Venue.owner_id == owner_id)
        if status is not None:
            stmt = stmt.where(Venue.status == status)
        if category_id is not None:
            stmt = stmt.where(Venue.category_id == category_id)
        if subcategory_id is not None:
            stmt = stmt.where(Venue.subcategory_id == subcategory_id)
        if region_id is not None:
            stmt = stmt.where(Venue.region_id == region_id)

        stmt = stmt.offset(offset).limit(limit)
        return (await self.session.scalars(stmt)).all()

    async def get_by_id(self, id: int) -> Venue | None:
        return await self.session.scalar(
            select(Venue)
            .options(
                selectinload(Venue.owner),
                selectinload(Venue.region),
                selectinload(Venue.category),
                selectinload(Venue.subcategory),
                selectinload(Venue.photos),
                selectinload(Venue.social_medias),
                selectinload(Venue.feedbacks),
            )
            .where(Venue.id == id)
            .where(Venue.is_deleted.is_(False))
        )