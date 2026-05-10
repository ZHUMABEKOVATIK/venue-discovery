from src.repositories.refresh_token import RefreshTokenRepository
from src.schemas.session import SessionOut
from src.core.exceptions import NotFoundException


class SessionService:
    def __init__(self, token_repo: RefreshTokenRepository):
        self.token_repo = token_repo

    async def get_sessions(self, user_id: int, current_token: str) -> list[SessionOut]:
        sessions = await self.token_repo.get_active_sessions(user_id)
        return [
            SessionOut(
                id=s.id,
                user_agent=s.user_agent,
                ip_address=s.ip_address,
                created_at=s.created_at,
                expires_at=s.expires_at,
                is_current=s.token == current_token,
            )
            for s in sessions
        ]

    async def revoke_session(self, session_id: int, user_id: int) -> None:
        success = await self.token_repo.revoke_by_id(session_id, user_id)
        if not success:
            raise NotFoundException("Session not found")

    async def revoke_all_except_current(self, user_id: int, current_token: str) -> None:
        await self.token_repo.revoke_all_except(user_id, current_token)