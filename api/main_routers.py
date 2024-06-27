from api.api_meals.routers import meals_router
from fastapi import APIRouter


mainRouter = APIRouter(
    prefix="/api/v1"
)

mainRouter.include_router(meals_router)
