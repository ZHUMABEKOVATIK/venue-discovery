from fastapi import APIRouter, Depends
from src.dependencies import AuthServiceDep
from src.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest, LogoutRequest
from src.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])