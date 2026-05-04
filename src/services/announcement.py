from src.repositories.announcement import AnnouncementRepo
from src.models.announcement import Announcement
from src.core.exceptions import NotFoundException, BadRequestException
from src.models.model_enums import DataStatus

from src.utils.file_handler import save_image, delete_image
from fastapi import UploadFile

class AnnouncementService:
    def __init__(self, repo: AnnouncementRepo):
        self.repo = repo

    async def get_all(
        self,
        *,
        user_id: int | None = None,
        only_approved: bool = False,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[Announcement]:
        return await self.repo.get_all(
            user_id = user_id,
            only_approved=only_approved,
            offset=offset,
            limit=limit
        )
    
    async def create(self, user_id: int, photo: UploadFile, value: str, description: str | None) -> Announcement:
        photo_url = await save_image(photo, folder="announcements")

        obj = Announcement(
            user_id=user_id,
            photo_url=photo_url,
            value=value,
            description=description,
        )
        return await self.repo.create(obj)
    
    async def update_photo(self, id: int, user_id: int, photo: UploadFile) -> Announcement:
        data = await self.repo.get_by_id(id=id)
        if data is None:
            raise NotFoundException("Announcement not found")
        
        if data.user_id != user_id:
            raise BadRequestException("Sizge tiyisli bolmag'an anons")
        
        photo_url = await save_image(photo, folder="announcements")

        return await self.repo.update(id, photo_url=photo_url)

    async def update_body(self, id: int, user_id: int, value: str, description: str | None) -> Announcement:
        data = await self.repo.get_by_id(id=id)
        if data is None:
            raise NotFoundException("Announcement not found")
        
        if data.user_id != user_id:
            raise BadRequestException("Sizge tiyisli bolmag'an anons")
        
        if data.status == DataStatus.approved or data.status == DataStatus.rejected:
            raise BadRequestException("Bul Anons qabillang'ansin yaki biykarlang'ansin o'zgermeydi")
        
        updates = {"status": DataStatus.revision}
        
        if value is not None:
            updates["value"] = value

        if description is not None:
            updates["description"] = description
        
        return await self.repo.update(id, **updates)
    
    async def approve_announcement(self, annons_id: int) -> Announcement:
        return await self.repo.update(id=annons_id, status=DataStatus.approved)
    
    async def rejected_announcement(self, annons_id: int, comment: str) -> Announcement:
        return await self.repo.update(id=annons_id, status=DataStatus.rejected, comment=comment)
    
    async def revision_announcement(self, annons_id: int, comment: str) -> Announcement: 
        return await self.repo.update(id=annons_id, status=DataStatus.revision, comment=comment)
    
    async def delete(self, id: int) -> None:
        data = await self.repo.get_by_id(id=id)
        if data is None:
            raise NotFoundException("Announcement not found")
        if data.is_deleted == True:
            raise NotFoundException("Announcement not found")
        await self.repo.delete(data)