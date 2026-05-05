from fastapi import APIRouter

from .auth import router as auth_router
from .region import router as region_router
from .contact_message import router as contact_msg_router
from .category import router as category_router
from .user import router as user_router
from .announcement import router as announcement_router
from .feedback import router as feedback_router
from .advertising import router as advertising_router

routers_v1 = APIRouter(prefix="/v1")

routers_v1.include_router(auth_router)
routers_v1.include_router(user_router)
routers_v1.include_router(region_router)
routers_v1.include_router(category_router)
routers_v1.include_router(contact_msg_router)
routers_v1.include_router(feedback_router)
routers_v1.include_router(announcement_router)
routers_v1.include_router(advertising_router)
