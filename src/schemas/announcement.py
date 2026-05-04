from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.models.model_enums import DataStatus


class UserShortOut(BaseModel):
    id: int
    first_name: str
    last_name: str | None

    model_config = ConfigDict(from_attributes=True)


class AnnouncementOut(BaseModel):
    id: int
    user: UserShortOut
    photo_url: str
    value: str
    description: str | None
    status: DataStatus
    comment: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnnouncementGet(BaseModel):
    only_approved: bool
    offset: int
    limit: int