from datetime import datetime, timedelta, timezone
from uuid import UUID

from src.repositories.user import UserRepository
from src.repositories.refresh_token import RefreshTokenRepository
from src.models.user import User
from src.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from src.core.jwt import create_access_token, create_refresh_token, verify_refresh_token
from src.core.security import hash_password, verify_password
from src.core.config import settings
from src.core.exceptions import BadRequestException, UnauthorizedException


class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: RefreshTokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def register(self, payload: RegisterRequest) -> TokenResponse:
        already_exists = await self.user_repo.is_exists(
            username=payload.username, email=payload.email
        )
        if already_exists:
            raise BadRequestException("username или email уже занят")

        user = User(
            username=payload.username,
            email=payload.email,
            hashed_password=hash_password(payload.password),
            display_name=payload.display_name,
        )
        user = await self.user_repo.create(user)
        return await self._issue_tokens(user.id)

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_one(email=payload.login)
        if user is None:
            user = await self.user_repo.get_one(username=payload.login)
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise BadRequestException("неверный логин или пароль")

        return await self._issue_tokens(user.id)

    async def refresh(self, token: str) -> TokenResponse:
        payload = verify_refresh_token(token)
        if payload is None:
            raise UnauthorizedException("невалидный токен")

        stored = await self.token_repo.get_by_token(token)
        if stored is None:
            raise UnauthorizedException("токен отозван или истёк")

        await self.token_repo.revoke(stored)
        return await self._issue_tokens(stored.user_id)

    async def logout(self, token: str) -> None:
        stored = await self.token_repo.get_by_token(token)
        if stored is not None:
            await self.token_repo.revoke(stored)

    async def _issue_tokens(self, user_id: UUID) -> TokenResponse:
        access = create_access_token(data={"sub": str(user_id)})
        refresh = create_refresh_token(data={"sub": str(user_id)})

        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        await self.token_repo.create(
            user_id=user_id,
            token=refresh,
            expires_at=expires_at,
        )

        return TokenResponse(access_token=access, refresh_token=refresh)