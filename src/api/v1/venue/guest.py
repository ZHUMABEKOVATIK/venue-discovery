from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from src.dependencies import VenueServiceDep, CurrentUserDep
from src.schemas.venue import VenueGuestOut, VenueListOut
from src.core.exceptions import BadRequestException
from src.models.model_enums import DataStatus

router = APIRouter(prefix="/guest", tags=['Venues'])

@router.get("/all", response_model=list[VenueListOut])
async def get_venues(
    service: VenueServiceDep,
    user: CurrentUserDep,
    category_id: int | None = Query(None),
    subcategory_id: int | None = Query(None),
    region_id: int | None = Query(None),
    offset: int | None = Query(None),
    limit: int | None = Query(None),
):
    return await service.get_all_for_guest(
        category_id=category_id,
        subcategory_id=subcategory_id,
        region_id=region_id,
        offset=offset,
        limit=limit,
    )

@router.get("/detail/{venue_id}", response_model=VenueGuestOut)
async def get_venue(
    venue_id: int,
    user: CurrentUserDep,
    service: VenueServiceDep,
):
    return await service.get_one_for_guest(venue_id=venue_id, user_id=user.id)

@router.get("/qr/{venue_id}", response_class=StreamingResponse, description="Qr code usi api arqali aladi")
async def get_qr(venue_id: int, user: CurrentUserDep, service: VenueServiceDep):
    venue = await service.get_one(venue_id)
    if venue.status != DataStatus.approved:
        raise BadRequestException("Venue ele tastıyıqlanbaǵan")
    return service.generate_qr_response(user_id=user.id, venue_id=venue_id)