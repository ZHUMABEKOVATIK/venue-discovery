from src.repositories.region import RegionRepo
from src.models.region import Region
from src.core.exceptions import NotFoundException

class RegionService:
    def __init__(self, repo: RegionRepo):
        self.repo = repo
    
    async def create(self, name: str) -> Region:
        return await self.repo.create(Region(name=name.strip()))
    
    async def get_all(self) -> list[Region]:
        return await self.repo.get_all()
    
    async def update(self, id: int, name: str) -> Region:
        data = await self.repo.update(id=id, name=name)
        if data is None:
            raise NotFoundException("Region not found")
        return data
    
    async def delete(self, id: int) -> None:
        data = await self.repo.get_by_id(id)
        if data is None:
            raise NotFoundException("Region not found!")
        await self.repo.delete(data)