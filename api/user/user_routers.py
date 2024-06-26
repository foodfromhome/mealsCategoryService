from .user_main.api import router as user_main_router
from fastapi import APIRouter


user_router = APIRouter(
    tags=['Страница пользователя'],
)

user_router.include_router(user_main_router)
