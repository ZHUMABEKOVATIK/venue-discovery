from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sessions import get_async_session
from src.repositories.user import UserRepository
from src.services.user import UserService

def get_user_repo(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)

def get_user_service(repo: UserRepository = Depends(get_user_repo)) -> UserService:
    return UserService(repo)
