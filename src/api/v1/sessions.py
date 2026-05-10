from fastapi import APIRouter, status
from src.dependencies import CurrentUserDep, SessionServiceDep
from src.schemas.session import SessionOut, RevokeSessionIn

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.get("/", response_model=list[SessionOut], description="Sessiyalar dizimi")
async def get_sessions(user: CurrentUserDep, service: SessionServiceDep, current_token: RevokeSessionIn):
    return await service.get_sessions(user_id=user.id, current_token=current_token.refresh_token)

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT, description="Bir sessiyani shig'arip jiberiw")
async def revoke_session(session_id: int, user: CurrentUserDep, service: SessionServiceDep):
    await service.revoke_session(session_id=session_id, user_id=user.id)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, description="Qalg'an hamme sessiyalardi o'shiriw")
async def revoke_all_sessions(payload: RevokeSessionIn, user: CurrentUserDep, service: SessionServiceDep):
    await service.revoke_all_except_current(user_id=user.id, current_token=payload.refresh_token)