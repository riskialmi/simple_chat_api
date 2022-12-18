from fastapi import APIRouter

from app.api.routers import users, rooms

router = APIRouter()
router.include_router(users.router)
router.include_router(rooms.router)
