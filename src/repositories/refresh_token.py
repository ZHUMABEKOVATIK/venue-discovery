from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from src.models.refresh import RefreshToken

class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        self.session.add(refresh_token)
        await self.session.flush()
        return refresh_token

    async def get_by_token(self, token: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.is_revoked.is_(False),
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def revoke(self, token: RefreshToken) -> None:
        token.is_revoked = True
        await self.session.flush()

    async def revoke_all(self, user_id: int) -> None:
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked.is_(False),
        )
        tokens = (await self.session.scalars(stmt)).all()
        for token in tokens:
            token.is_revoked = True
        await self.session.flush()