from api.api_meals.api import router as add_meals_router
from fastapi import APIRouter


meals_router = APIRouter(
    tags=['Добавление, изменение, удаление и отображение блюд']
)


meals_router.include_router(add_meals_router)
