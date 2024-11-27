from fastapi import APIRouter

from app.endpoints.group import router as group_router
from app.endpoints.message import router as message_router
from app.endpoints.photo import router as photo_router
from app.endpoints.user_tg import router as user_tg_router

main_router = APIRouter()
main_router.include_router(user_tg_router)
main_router.include_router(group_router)
main_router.include_router(photo_router)
main_router.include_router(message_router)
