from fastapi import APIRouter

from app.endpoints import (
    group_router,
    message_router,
    photo_router,
    user_tg_router,
)

main_router = APIRouter()
main_router.include_router(user_tg_router)
main_router.include_router(group_router)
main_router.include_router(photo_router)
main_router.include_router(message_router)
