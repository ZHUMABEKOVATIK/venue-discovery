from fastapi import APIRouter, UploadFile, File, status

from src.dependencies import CurrentUserDep, VenueServiceDep
from src.models.model_enums import UserRole
from src.core.exceptions import BadRequestException
from src.schemas.venue import VenueOwnerOut, QRScanResult, QRScanIn, VenueIn, VenueUpdateIn

router = APIRouter(prefix="/owner", tags=['Venues'])

@router.post("/", response_model=VenueOwnerOut, status_code=status.HTTP_201_CREATED)
async def create_venue(
    user: CurrentUserDep,
    service: VenueServiceDep,
    payload: VenueIn
):
    if user.role != UserRole.owner:
        raise BadRequestException("Tek owner venue qosa aladi")
    return await service.create(owner_id=user.id, payload=payload)

@router.post("/{venue_id}/photos", status_code=201)
async def add_photo(
    venue_id: int,
    user: CurrentUserDep,
    service: VenueServiceDep,
    photo: UploadFile = File(...),
):
    if user.role != UserRole.owner:
        raise BadRequestException("Tek owner ushin")
    return await service.add_photo(venue_id=venue_id, owner_id=user.id, photo=photo)

@router.delete("/photos/{venue_id}/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(
    venue_id: int,
    photo_id: int,
    user: CurrentUserDep,
    service: VenueServiceDep,
):
    if user.role != UserRole.owner:
        raise BadRequestException("Tek owner ushin")
    await service.delete_photo(venue_id=venue_id, photo_id=photo_id, owner_id=user.id)

@router.get("/all", response_model=list[VenueOwnerOut])
async def get_my_venues(user: CurrentUserDep, service: VenueServiceDep):
    if user.role != UserRole.owner:
        raise BadRequestException("Tek owner ushin")
    
    return await service.get_my_venues(owner_id=user.id)

@router.patch("/{venue_id}", response_model=VenueOwnerOut)
async def update_venue(
    venue_id: int,
    payload: VenueUpdateIn,
    user: CurrentUserDep,
    service: VenueServiceDep,
):
    if user.role != UserRole.owner:
        raise BadRequestException("Tek owner ushin")
    return await service.update(venue_id=venue_id, owner_id=user.id, payload=payload)

@router.delete("/one/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_venue(venue_id: int, user: CurrentUserDep, service: VenueServiceDep):
    if user.role != UserRole.owner:
        raise BadRequestException("Tek owner ushin")
    await service.delete(venue_id=venue_id, owner_id=user.id)

# ------------------------------------------- Scanning -----------------------------------------------------

@router.post("/scan", response_model=QRScanResult)
async def scan_qr(
    payload: QRScanIn,
    user: CurrentUserDep,
    service: VenueServiceDep,
):
    if user.role != UserRole.owner:
        raise BadRequestException("Tek owner skanerlew mumkin")
    return await service.scan_qr(
        user_id=payload.user_id,
        venue_id=payload.venue_id,
        owner_id=user.id,
    )