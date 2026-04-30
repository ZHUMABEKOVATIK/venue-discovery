from .base_repository import BaseRepository

from src.models.region import Region

class RegionRepo(BaseRepository[Region]):
    model = Region
