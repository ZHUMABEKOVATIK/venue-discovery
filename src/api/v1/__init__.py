from fastapi import APIRouter

from .contact_message import router as contact_msg_router

routers_v1 = APIRouter(prefix="/v1")

routers_v1.include_router(contact_msg_router)