from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sessions import get_async_session
from src.repositories.advertising import AdvertisingRepo
from src.services.advertising import AdvertisingService

def get_advertising_repo(session: AsyncSession = Depends(get_async_session)) -> AdvertisingRepo:
    return AdvertisingRepo(session)

def get_advertising_service(repo: AdvertisingRepo = Depends(get_advertising_repo)) -> AdvertisingService:
    return AdvertisingService(repo)