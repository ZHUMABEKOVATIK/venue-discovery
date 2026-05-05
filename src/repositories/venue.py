from .base_repository import BaseRepository
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.venue import Venue

class AdvertisingRepo(BaseRepository[Venue]):
    model = Venue

