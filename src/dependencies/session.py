from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.sessions import get_async_session
from src.repositories.refresh_token import RefreshTokenRepository
from src.services.session import SessionService


def get_session_service(session: AsyncSession = Depends(get_async_session)) -> SessionService:
    return SessionService(token_repo=RefreshTokenRepository(session))