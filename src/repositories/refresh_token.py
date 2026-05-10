from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from src.models.refresh import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, token: str, expires_at: datetime,
                     user_agent: str | None = None, ip_address: str | None = None) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id, token=token, expires_at=expires_at,
            user_agent=user_agent, ip_address=ip_address,
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

    async def get_by_id(self, token_id: int, user_id: int) -> RefreshToken | None:
        return await self.session.scalar(
            select(RefreshToken).where(
                RefreshToken.id == token_id,
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
            )
        )

    async def get_active_sessions(self, user_id: int) -> list[RefreshToken]:
        stmt = (
            select(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
                RefreshToken.expires_at > datetime.now(timezone.utc),
            )
            .order_by(RefreshToken.created_at.desc())
        )
        return (await self.session.scalars(stmt)).all()

    async def revoke(self, token: RefreshToken) -> None:
        token.is_revoked = True
        await self.session.flush()

    async def revoke_by_id(self, token_id: int, user_id: int) -> bool:
        token = await self.get_by_id(token_id, user_id)
        if token is None:
            return False
        token.is_revoked = True
        await self.session.flush()
        return True

    async def revoke_all(self, user_id: int) -> None:
        tokens = (await self.session.scalars(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
            )
        )).all()
        for token in tokens:
            token.is_revoked = True
        await self.session.flush()

    async def revoke_all_except(self, user_id: int, current_token: str) -> None:
        tokens = (await self.session.scalars(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
                RefreshToken.token != current_token,
            )
        )).all()
        for token in tokens:
            token.is_revoked = True
        await self.session.flush()