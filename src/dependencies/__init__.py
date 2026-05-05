from typing import Annotated
from fastapi import Depends

from .auth import get_current_user, get_auth_service
from .user import get_user_service
from .contact_message import get_contact_message_service
from .region import get_region_service
from .category import get_category_service, get_subcategory_service
from .feedback import get_feedback_service
from .announcement import get_announcement_service
from .advertising import get_advertising_service

from src.models.user import User, UserRole

from src.services import (
    UserService, 
    AuthService, 
    ContactMessageService, 
    RegionService, 
    CategoryService, 
    SubCategoryService, 
    FeedbackService,
    AnnouncementService,
    AdvertisingService
)

from src.core.exceptions import BadRequestException

CurrentUserDep = Annotated[User, Depends(get_current_user)]

def require_admin(user: CurrentUserDep) -> CurrentUserDep:
    if user.role != UserRole.admin:
        raise BadRequestException("Bul soraw tek admin ushin")
    return user

AdminDep = Annotated[User, Depends(require_admin)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
ContactMessageServiceDep = Annotated[ContactMessageService, Depends(get_contact_message_service)]
RegionServiceDep = Annotated[RegionService, Depends(get_region_service)]
CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
SubCategoryServiceDep = Annotated[SubCategoryService, Depends(get_subcategory_service)]
FeedbackServiceDep = Annotated[FeedbackService, Depends(get_feedback_service)]
AnnouncementServiceDep = Annotated[AnnouncementService, Depends(get_announcement_service)]
AdvertisingServiceDep = Annotated[AdvertisingService, Depends(get_advertising_service)]