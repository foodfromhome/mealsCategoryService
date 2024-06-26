from api.admin.add_meals.api import router as add_meals_router
from api.admin.admin_main.api import router as admin_main_router
from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1",
)


router.include_router(add_meals_router)
router.include_router(admin_main_router)
