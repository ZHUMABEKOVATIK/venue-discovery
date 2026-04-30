from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sessions import get_async_session
from src.repositories.region import RegionRepo
from src.services.region import RegionService

def get_region_repo(session: AsyncSession = Depends(get_async_session)) -> RegionRepo:
    return RegionRepo(session)

def get_region_service(repo: RegionRepo = Depends(get_region_repo)) -> RegionService:
    return RegionService(repo)