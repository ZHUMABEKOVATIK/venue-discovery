from src.repositories.advertising import AdvertisingRepo
from src.models.advertising import Advertising
from src.core import NotFoundException

from fastapi import UploadFile

from src.utils.file_handler import save_image, delete_image

class AdvertisingService:
    def __init__(self, repo: AdvertisingRepo):
        self.repo = repo

    async def create(self, category_id: int, photo: UploadFile, title: str, description: str) -> Advertising:
        photo_url = await save_image(photo, folder="advertising")
        data = Advertising(
            category_id=category_id,
            photo_url=photo_url,
            title=title,
            description=description
        )
        return await self.repo.create(data)
    
    async def get_all(self) -> list[Advertising]:
        return await self.repo.get_all()
    
    async def update_photo(self, ad_id: int, photo: UploadFile) -> Advertising:
        data = await self.repo.get_by_id(ad_id)
        if data is None:
            raise NotFoundException("Advertising not found")
        
        delete_image(data.photo_url)
        
        photo_url = await save_image(photo, folder="advertising")

        return await self.repo.update(id=ad_id, photo_url=photo_url)
    
    async def update_body(self, ad_id: int, title: str, description: str, category_id: int) -> Advertising:
        data = await self.repo.get_by_id(ad_id)
        if data is None:
            raise NotFoundException("Advertising not found")
        
        updates = {}

        if title is not None:
            updates["title"] = title

        if description is not None:
            updates["description"] = description
        
        if category_id is not None:
            updates["category_id"] = category_id
        
        return await self.repo.update(ad_id, **updates)
        
    async def delete(self, ad_id: int) -> None:
        data = await self.repo.get_by_id(ad_id)
        if data is None:
            raise NotFoundException("Advertising not found")
        
        await self.repo.delete(data)
