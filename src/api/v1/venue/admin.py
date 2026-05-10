from fastapi import APIRouter, Query

from src.dependencies import AdminDep, VenueServiceDep
from src.schemas.venue import AdminReviewIn, VenueAdminOut
from src.models.model_enums import DataStatus

router = APIRouter(prefix="/admin", tags=['Venues'])

@router.get("/all", response_model=list[VenueAdminOut])
async def admin_get_all(
    _: AdminDep,
    service: VenueServiceDep,
    status: DataStatus | None = Query(None),
    offset: int | None = Query(None),
    limit: int | None = Query(None),
):
    return await service.get_all_for_admin(status=status, offset=offset, limit=limit)


@router.patch("/{venue_id}/review", response_model=VenueAdminOut)
async def admin_review(
    venue_id: int,
    payload: AdminReviewIn,
    _: AdminDep,
    service: VenueServiceDep,
):
    return await service.review(venue_id=venue_id, payload=payload)
