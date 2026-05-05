from pydantic import BaseModel, Field, ConfigDict
from datetime import time
from decimal import Decimal
from src.models.model_enums import DataStatus


class UserShortOut(BaseModel):
    id: int
    first_name: str
    last_name: str | None

    model_config = ConfigDict(from_attributes=True)


class RegionShortOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryShortOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# ── INPUT ──────────────────────────────────────────────────────

class VenueIn(BaseModel):
    name_kr: str
    name_ru: str
    name_en: str
    name_uz: str
    description_kr: str | None = None
    description_ru: str | None = None
    description_en: str | None = None
    description_uz: str | None = None
    region_id: int
    category_id: int
    subcategory_id: int | None = None
    days_of_week: list[int] = Field(..., description="Ha'pte ku'nleri [1-7]")
    open_time: time | None = None
    close_time: time | None = None
    is_always_open: bool = False
    is_closed: bool = False
    phone: str | None = None
    address_kr: str | None = None
    address_ru: str | None = None
    address_en: str | None = None
    address_uz: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    visit_amount: int = Field(5, description="Neshe ma'rte kelgennen keyin skidka")
    promotion_percentage: int = Field(5, description="Neshe procent skidka")


class VenueUpdateIn(BaseModel):
    name_kr: str | None = None
    name_ru: str | None = None
    name_en: str | None = None
    name_uz: str | None = None
    description_kr: str | None = None
    description_ru: str | None = None
    description_en: str | None = None
    description_uz: str | None = None
    region_id: int | None = None
    category_id: int | None = None
    subcategory_id: int | None = None
    days_of_week: list[int] | None = None
    open_time: time | None = None
    close_time: time | None = None
    is_always_open: bool | None = None
    is_closed: bool | None = None
    phone: str | None = None
    address_kr: str | None = None
    address_ru: str | None = None
    address_en: str | None = None
    address_uz: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    visit_amount: int | None = None
    promotion_percentage: int | None = None


# ── OUTPUT ─────────────────────────────────────────────────────

class VenueListOut(BaseModel):
    """Список заведений — краткая карточка"""
    id: int
    name_uz: str | None
    name_ru: str | None
    name_kr: str | None
    address_uz: str | None
    address_ru: str | None
    region: RegionShortOut | None
    category: CategoryShortOut | None
    rating: float | None = None
    feedback_count: int | None = None

    model_config = ConfigDict(from_attributes=True)


class VenueAdminOut(BaseModel):
    """Для админа — видит всё включая статус и комментарий"""
    id: int
    owner: UserShortOut
    name_kr: str | None
    name_ru: str | None
    name_en: str | None
    name_uz: str | None
    description_kr: str | None
    description_ru: str | None
    description_en: str | None
    description_uz: str | None
    region: RegionShortOut | None
    category: CategoryShortOut | None
    subcategory: CategoryShortOut | None
    days_of_week: int | None
    open_time: str | None
    close_time: str | None
    is_always_open: bool
    is_closed: bool
    phone: str | None
    address_kr: str | None
    address_ru: str | None
    address_en: str | None
    address_uz: str | None
    latitude: Decimal | None
    longitude: Decimal | None
    visit_amount: int
    promotion_percentage: int
    status: DataStatus
    comment: str | None

    model_config = ConfigDict(from_attributes=True)


class VenueOwnerOut(BaseModel):
    """Для owner — видит только своё заведение со статусом"""
    id: int
    name_kr: str | None
    name_ru: str | None
    name_en: str | None
    name_uz: str | None
    description_kr: str | None
    description_ru: str | None
    description_en: str | None
    description_uz: str | None
    region: RegionShortOut | None
    category: CategoryShortOut | None
    subcategory: CategoryShortOut | None
    days_of_week: int | None
    open_time: str | None
    close_time: str | None
    is_always_open: bool
    is_closed: bool
    phone: str | None
    address_kr: str | None
    address_ru: str | None
    address_en: str | None
    address_uz: str | None
    latitude: Decimal | None
    longitude: Decimal | None
    visit_amount: int
    promotion_percentage: int
    status: DataStatus
    comment: str | None

    model_config = ConfigDict(from_attributes=True)


class VenueGuestOut(BaseModel):
    """Для guest — детальная страница заведения без служебных полей"""
    id: int
    name_uz: str | None
    name_ru: str | None
    name_kr: str | None
    description_uz: str | None
    description_ru: str | None
    description_kr: str | None
    region: RegionShortOut | None
    category: CategoryShortOut | None
    subcategory: CategoryShortOut | None
    days_of_week: int | None
    open_time: str | None
    close_time: str | None
    is_always_open: bool
    is_closed: bool
    phone: str | None
    address_uz: str | None
    address_ru: str | None
    address_kr: str | None
    latitude: Decimal | None
    longitude: Decimal | None
    rating: float | None = None
    feedback_count: int | None = None

    model_config = ConfigDict(from_attributes=True)


class QRScanResult(BaseModel):
    """Результат сканирования QR — owner видит это"""
    user_id: int
    first_name: str
    last_name: str | None
    visit_count: int               # сколько раз посетил
    visit_amount_required: int     # сколько нужно для скидки
    discount_percentage: int       # 0 если ещё не достиг порога
    can_give_discount: bool        # visit_count >= visit_amount_required


class AdminReviewIn(BaseModel):
    """Админ одобряет / отклоняет / отправляет на revision"""
    status: DataStatus
    comment: str | None = None

class QRScanIn(BaseModel):
    user_id: int
    venue_id: int