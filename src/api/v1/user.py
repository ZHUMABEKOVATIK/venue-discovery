from fastapi import APIRouter, status
from src.dependencies import CurrentUserDep, UserServiceDep
from src.schemas.user import UserOut, UserUpdateRequest
from src.schemas.auth import LogoutRequest
from src.dependencies import AuthServiceDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
async def get_me(user: CurrentUserDep, service: UserServiceDep):
    return await service.get_me(user.id)


@router.patch("/me", response_model=UserOut)
async def update_me(
    payload: UserUpdateRequest,
    user: CurrentUserDep,
    service: UserServiceDep,
):
    return await service.update_me(user.id, payload)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    payload: LogoutRequest,
    user: CurrentUserDep,
    user_service: UserServiceDep,
    auth_service: AuthServiceDep,
):
    await auth_service.logout(payload.refresh_token)
    await user_service.delete_me(user.id)
