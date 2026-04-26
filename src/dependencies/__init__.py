from typing import Annotated
from fastapi import Depends

from .auth import get_current_user, get_auth_service
from .user import get_user_service
from .contact_message import get_contact_message_service

from src.models.user import User, UserRole
from src.services.user import UserService
from src.services.auth import AuthService
from src.services.contact_message import ContactMessageService

from src.core.exceptions import BadRequestException

def require_admin(user: CurrentUserDep):
    if user.role != UserRole.admin:
        raise BadRequestException("Bul soraw tek admin ushin")
    return user

AdminDep = Annotated[User, Depends(require_admin)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
ContactMessageServiceDep = Annotated[ContactMessageService, Depends(get_contact_message_service)]