from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from ..db.sessions import get_async_session
from ..repositories.user import UserRepository
from ..repositories.refresh_token import RefreshTokenRepository
from ..services.auth import AuthService
from ..models.user import User
from ..core.jwt import verify_access_token

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    token = credentials.credentials
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = await UserRepository(session).get_one(_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

def get_auth_service(session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(
        user_repo=UserRepository(session),
        token_repo=RefreshTokenRepository(session),
    )