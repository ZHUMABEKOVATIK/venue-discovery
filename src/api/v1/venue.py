from fastapi import APIRouter, Query, Form, File, UploadFile, status
from fastapi.responses import StreamingResponse

from src.dependencies import CurrentUserDep, AdminDep, VenueServiceDep
from src.models.model_enums import DataStatus, UserRole
from src.core.exceptions import BadRequestException
from src.schemas.venue import (
    VenueIn, VenueUpdateIn, AdminReviewIn,
    VenueListOut, VenueGuestOut, VenueOwnerOut, VenueAdminOut, QRScanResult, QRScanIn
)

router = APIRouter(prefix="/venues", tags=["Venues"])


# ── GUEST — список одобренных заведений ────────────────────────

@router.get("/", response_model=list[VenueListOut])
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

# ── OWNER — создать заведение ──────────────────────────────────

@router.post("/", response_model=VenueOwnerOut, status_code=status.HTTP_201_CREATED)
async def create_venue(
    user: CurrentUserDep,
    service: VenueServiceDep,
    payload: VenueIn,
):
    if user.role != UserRole.owner:
        raise BadRequestException("Tek owner venue qosa aladi")
    return await service.create(owner_id=user.id, payload=payload)


# ── OWNER — свои заведения ─────────────────────────────────────

@router.get("/my/venues", response_model=list[VenueOwnerOut])
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


@router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_venue(venue_id: int, user: CurrentUserDep, service: VenueServiceDep):
    if user.role != UserRole.owner:
        raise BadRequestException("Tek owner ushin")
    await service.delete(venue_id=venue_id, owner_id=user.id)


# ── OWNER — сканирует QR гостя ─────────────────────────────────

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


# ── ADMIN ──────────────────────────────────────────────────────

@router.get("/admin/all", response_model=list[VenueAdminOut])
async def admin_get_all(
    _: AdminDep,
    service: VenueServiceDep,
    status: DataStatus | None = Query(None),
    offset: int | None = Query(None),
    limit: int | None = Query(None),
):
    return await service.get_all_for_admin(status=status, offset=offset, limit=limit)


@router.patch("/admin/{venue_id}/review", response_model=VenueAdminOut)
async def admin_review(
    venue_id: int,
    payload: AdminReviewIn,
    _: AdminDep,
    service: VenueServiceDep,
):
    return await service.review(venue_id=venue_id, payload=payload)

# ── GUEST — детальная страница заведения + QR ──────────────────

@router.get("/my/{venue_id}", response_model=VenueGuestOut)
async def get_venue(venue_id: int, service: VenueServiceDep):
    return await service.get_one(venue_id)


@router.get("/{venue_id}/qr", response_class=StreamingResponse)
async def get_qr(venue_id: int, user: CurrentUserDep, service: VenueServiceDep):
    """
    Guest открывает страницу заведения → видит свой QR код.
    QR генерируется в памяти, не сохраняется.
    """
    venue = await service.get_one(venue_id)
    if venue.status != DataStatus.approved:
        raise BadRequestException("Venue ele tastıyıqlanbaǵan")
    return service.generate_qr_response(user_id=user.id, venue_id=venue_id)