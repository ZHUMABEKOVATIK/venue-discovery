from datetime import datetime, timedelta, timezone

from src.repositories.user import UserRepository
from src.repositories.refresh_token import RefreshTokenRepository
from src.models.user import User
from src.models.model_enums import UserRole
from src.schemas.auth import GuestRegisterRequest, OwnerRegisterRequest, LoginRequest, TokenResponse
from src.core.jwt import create_access_token, create_refresh_token, verify_refresh_token
from src.core.security import hash_password, verify_password
from src.core.config import settings
from src.core.exceptions import BadRequestException, UnauthorizedException


class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: RefreshTokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def register_guest(self, payload: GuestRegisterRequest) -> TokenResponse:
        return await self._register(payload, role=UserRole.guest)

    async def register_owner(self, payload: OwnerRegisterRequest) -> TokenResponse:
        return await self._register(payload, role=UserRole.owner)

    async def _register(self, payload: GuestRegisterRequest | OwnerRegisterRequest, role: UserRole) -> TokenResponse:
        already_exists = await self.user_repo.is_exists(email=payload.email)
        if already_exists:
            raise BadRequestException("Bu email allaqachon band")

        user = User(
            email=payload.email,
            hashed_pw=hash_password(payload.password),
            first_name=payload.first_name,
            last_name=payload.last_name,
            role=role,
        )
        user = await self.user_repo.create(user)
        return await self._issue_tokens(user.id)

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_one(email=payload.email)
        if user is None or not verify_password(payload.password, user.hashed_pw):
            raise BadRequestException("Email yoki parol noto'g'ri")

        if not user.is_active:
            raise BadRequestException("Akkaunt bloklangan")

        return await self._issue_tokens(user.id)

    async def refresh(self, token: str) -> TokenResponse:
        payload = verify_refresh_token(token)
        if payload is None:
            raise UnauthorizedException("Token yaroqsiz")

        stored = await self.token_repo.get_by_token(token)
        if stored is None:
            raise UnauthorizedException("Token bekor qilingan yoki muddati o'tgan")

        await self.token_repo.revoke(stored)
        return await self._issue_tokens(stored.user_id)

    async def logout(self, token: str) -> None:
        stored = await self.token_repo.get_by_token(token)
        if stored is not None:
            await self.token_repo.revoke(stored)

    async def _issue_tokens(self, user_id: int) -> TokenResponse:
        access = create_access_token(data={"sub": str(user_id)})
        refresh = create_refresh_token(data={"sub": str(user_id)})

        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        await self.token_repo.create(
            user_id=user_id,
            token=refresh,
            expires_at=expires_at,
        )

        return TokenResponse(access_token=access, refresh_token=refresh)
