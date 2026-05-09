import io
import qrcode

from fastapi import UploadFile
from fastapi.responses import StreamingResponse

from src.repositories.venue import VenueRepo
from src.repositories.visits import VisitRepo
from src.models.venue import Venue
from src.models.venue_photos import VenuePhotos
from src.models.model_enums import DataStatus
from src.schemas.venue import VenueIn, VenueUpdateIn, AdminReviewIn, QRScanResult
from src.utils.file_handler import save_image, delete_image
from src.utils.scheduling import days_to_int
from src.core.exceptions import NotFoundException, BadRequestException


class VenueService:
    def __init__(self, venue_repo: VenueRepo, visit_repo: VisitRepo):
        self.venue_repo = venue_repo
        self.visit_repo = visit_repo

    async def create(self, owner_id: int, payload: VenueIn, photo: UploadFile | None = None) -> Venue:
        venue = Venue(
            owner_id=owner_id,
            name_kr=payload.name_kr,
            name_ru=payload.name_ru,
            name_en=payload.name_en,
            name_uz=payload.name_uz,
            description_kr=payload.description_kr,
            description_ru=payload.description_ru,
            description_en=payload.description_en,
            description_uz=payload.description_uz,
            region_id=payload.region_id,
            category_id=payload.category_id,
            subcategory_id=payload.subcategory_id,
            day_of_week=days_to_int(payload.days_of_week),
            open_time=str(payload.open_time) if payload.open_time else None,
            close_time=str(payload.close_time) if payload.close_time else None,
            is_always_open=payload.is_always_open,
            is_closed=payload.is_closed,
            phone=payload.phone,
            address_kr=payload.address_kr,
            address_ru=payload.address_ru,
            address_en=payload.address_en,
            address_uz=payload.address_uz,
            latitude=payload.latitude,
            longitude=payload.longitude,
            visit_amount=payload.visit_amount,
            promotion_percentage=payload.promotion_percentage,
            status=DataStatus.new,
        )
        await self.venue_repo.create(venue)
    
        if photo:
            photo_url = await save_image(photo, folder="venues")
            venue_photo = VenuePhotos(venue_id=venue.id, url=photo_url)
            self.venue_repo.session.add(venue_photo)
            await self.venue_repo.session.flush()
        
        return venue

    async def get_all_for_admin(self, status: DataStatus | None = None, offset: int | None = None, limit: int | None = None) -> list[Venue]:
        return await self.venue_repo.get_all(status=status, offset=offset, limit=limit)

    async def get_all_for_guest(self, category_id: int | None = None, subcategory_id: int | None = None, region_id: int | None = None, offset: int | None = None, limit: int | None = None) -> list[Venue]:
        """Только approved заведения"""
        return await self.venue_repo.get_all(
            status=DataStatus.approved,
            category_id=category_id,
            subcategory_id=subcategory_id,
            region_id=region_id,
            offset=offset,
            limit=limit,
        )

    async def get_my_venues(self, owner_id: int) -> list[Venue]:
        """Owner видит только свои"""
        return await self.venue_repo.get_all(owner_id=owner_id)

    async def get_one(self, venue_id: int) -> Venue:
        venue = await self.venue_repo.get_by_id(venue_id)
        if venue is None:
            raise NotFoundException(f"Venue with id {venue_id} not found")
        return venue

    async def update(self, venue_id: int, owner_id: int, payload: VenueUpdateIn) -> Venue:
        venue = await self.get_one(venue_id)
        if venue.owner_id != owner_id:
            raise BadRequestException("Bul sizge tiyisli emes")

        data = payload.model_dump(exclude_none=True)
        if "days_of_week" in data:
            data["day_of_week"] = days_to_int(data.pop("days_of_week"))

        return await self.venue_repo.update(venue_id, **data)

    async def delete(self, venue_id: int, owner_id: int) -> None:
        venue = await self.get_one(venue_id)
        if venue.owner_id != owner_id:
            raise BadRequestException("Bul sizge tiyisli emes")
        await self.venue_repo.delete(venue)

    async def add_photo(self, venue_id: int, owner_id: int, photo: UploadFile) -> VenuePhotos:
        venue = await self.get_one(venue_id)
        if venue.owner_id != owner_id:
            raise BadRequestException("Bul sizge tiyisli emes")

        photo_url = await save_image(photo, folder="venues")
        venue_photo = VenuePhotos(venue_id=venue_id, url=photo_url)
        self.venue_repo.session.add(venue_photo)
        await self.venue_repo.session.flush()
        return venue_photo

    async def delete_photo(self, photo_id: int, owner_id: int) -> None:
        photo = await self.venue_repo.session.get(VenuePhotos, photo_id)
        if photo is None:
            raise NotFoundException("Photo not found")
        
        venue = await self.get_one(photo.venue_id)
        if venue.owner_id != owner_id:
            raise BadRequestException("Bul sizge tiyisli emes")
    
        delete_image(photo.url)
        await self.venue_repo.session.delete(photo)
        await self.venue_repo.session.flush()

    async def get_one_for_guest(self, venue_id: int, user_id: int) -> dict:
        venue = await self.get_one(venue_id)
        if venue.status != DataStatus.approved:
            raise NotFoundException(f"Venue with id {venue_id} not found")

        visit = await self.visit_repo.get_by_user_and_venue(
            user_id=user_id,
            venue_id=venue_id,
        )
        visit_count = visit.amount if visit else 0
    
        venue_data = {
            "id": venue.id,
            "name_uz": venue.name_uz,
            "name_ru": venue.name_ru,
            "name_kr": venue.name_kr,
            "description_uz": venue.description_uz,
            "description_ru": venue.description_ru,
            "description_kr": venue.description_kr,
            "region": venue.region,
            "category": venue.category,
            "subcategory": venue.subcategory,
            "days_of_week": venue.day_of_week,
            "open_time": venue.open_time,
            "close_time": venue.close_time,
            "is_always_open": venue.is_always_open,
            "is_closed": venue.is_closed,
            "phone": venue.phone,
            "address_uz": venue.address_uz,
            "address_ru": venue.address_ru,
            "address_kr": venue.address_kr,
            "latitude": venue.latitude,
            "longitude": venue.longitude,
            "visit_count": visit_count,
        }
        return venue_data

    # ── ADMIN ──────────────────────────────────────────────────

    async def review(self, venue_id: int, payload: AdminReviewIn) -> Venue:
        """Админ одобряет / отклоняет / revision"""
        venue = await self.get_one(venue_id)
        venue.status = payload.status
        venue.comment = payload.comment
        await self.venue_repo.session.flush()
        return venue

    # ── QR код (динамический, без сохранения) ──────────────────

    def generate_qr_response(self, user_id: int, venue_id: int) -> StreamingResponse:
        """
        Генерирует QR код в памяти и возвращает как PNG.
        QR содержит: /api/v1/venues/scan?user_id=X&venue_id=Y
        Owner сканирует → попадает на эндпоинт scan
        """
        data = f"user_id={user_id}&venue_id={venue_id}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    # ── SCAN QR (owner сканирует) ──────────────────────────────

    async def scan_qr(self, user_id: int, venue_id: int, owner_id: int) -> QRScanResult:
        """
        Owner сканирует QR гостя:
        1. Проверяем что venue принадлежит этому owner
        2. +1 к visit.amount
        3. Возвращаем инфо о скидке
        """
        venue = await self.get_one(venue_id)
        if venue.owner_id != owner_id:
            raise BadRequestException("Bul sizge tiyisli emes")
        if venue.status != DataStatus.approved:
            raise BadRequestException("Venue hali tasdiqlanmagan")

        # находим или создаём запись визита
        visit = await self.visit_repo.get_or_create(user_id=user_id, venue_id=venue_id)
        visit.amount += 1
        await self.visit_repo.session.flush()

        can_give = visit.amount >= venue.visit_amount
        discount = venue.promotion_percentage if can_give else 0
        actual_count = visit.amount

        if can_give:
            visit.amount = 0
        await self.visit_repo.session.flush()

        return QRScanResult(
            user_id=user_id,
            first_name=visit.user.first_name,
            last_name=visit.user.last_name,
            visit_count=actual_count,
            visit_amount_required=venue.visit_amount,
            discount_percentage=discount,
            can_give_discount=can_give,
        )