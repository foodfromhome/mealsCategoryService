from api.admin.add_meals.api import router as add_meals_router
from api.admin.admin_main.api import router as admin_main_router
from fastapi import APIRouter


admin_router = APIRouter(
    tags=['Страница повара']
)


admin_router.include_router(add_meals_router)
admin_router.include_router(admin_main_router)
