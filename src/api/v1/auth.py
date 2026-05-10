from fastapi import APIRouter, Request, status
from src.dependencies import AuthServiceDep
from src.schemas.auth import GuestRegisterRequest, OwnerRegisterRequest, LoginRequest, TokenResponse, RefreshRequest, LogoutRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register/guest", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_guest(payload: GuestRegisterRequest, service: AuthServiceDep, request: Request):
    return await service.register_guest(payload, request=request)

@router.post("/register/owner", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_owner(payload: OwnerRegisterRequest, service: AuthServiceDep, request: Request):
    return await service.register_owner(payload, request=request)

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, service: AuthServiceDep, request: Request):
    return await service.login(payload, request=request)

@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, service: AuthServiceDep, request: Request):
    return await service.refresh(payload.refresh_token, request=request)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(payload: LogoutRequest, service: AuthServiceDep):
    await service.logout(payload.refresh_token)