from fastapi import APIRouter

from .auth import router as auth_router
from .region import router as region_router
from .contact_message import router as contact_msg_router
from .category import router as category_router

routers_v1 = APIRouter(prefix="/v1")

routers_v1.include_router(auth_router)
routers_v1.include_router(region_router)
routers_v1.include_router(category_router)
routers_v1.include_router(contact_msg_router)