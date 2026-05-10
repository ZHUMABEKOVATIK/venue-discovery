from fastapi import APIRouter
from .admin import router as admin_router
from .owner import router as owner_router
from .guest import router as guest_router

router = APIRouter(prefix="/venue", tags=['Venues'])

router.include_router(admin_router)
router.include_router(owner_router)
router.include_router(guest_router)