from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sessions import get_async_session
from src.repositories.announcement import AnnouncementRepo
from src.services.announcement import AnnouncementService

def get_announcement_repo(session: AsyncSession = Depends(get_async_session)) -> AnnouncementRepo:
    return AnnouncementRepo(session)

def get_announcement_service(repo: AnnouncementRepo = Depends(get_announcement_repo)) -> AnnouncementService:
    return AnnouncementService(repo)