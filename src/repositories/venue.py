from .base_repository import SoftDeleteRepository
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.venue import Venue

class VenueRepo(SoftDeleteRepository[Venue]):
    model = Venue

