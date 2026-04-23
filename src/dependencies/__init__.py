from typing import Annotated
from fastapi import Depends

from .auth import get_current_user, get_auth_service
from .user import get_user_service
from src.models.user import User
from src.services.user import UserService
from src.services.auth import AuthService

CurrentUserDep = Annotated[User, Depends(get_current_user)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]