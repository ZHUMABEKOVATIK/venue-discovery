from fastapi import APIRouter
from src.dependencies import AuthServiceDep
from src.schemas.auth import (
    GuestRegisterRequest,
    OwnerRegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    LogoutRequest,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/guest", response_model=TokenResponse, status_code=201)
async def register_guest(payload: GuestRegisterRequest, service: AuthServiceDep):
    return await service.register_guest(payload)


@router.post("/register/owner", response_model=TokenResponse, status_code=201)
async def register_owner(payload: OwnerRegisterRequest, service: AuthServiceDep):
    return await service.register_owner(payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, service: AuthServiceDep):
    return await service.login(payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, service: AuthServiceDep):
    return await service.refresh(payload.refresh_token)


@router.post("/logout", status_code=204)
async def logout(payload: LogoutRequest, service: AuthServiceDep):
    await service.logout(payload.refresh_token)
