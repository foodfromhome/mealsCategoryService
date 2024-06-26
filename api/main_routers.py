from api.admin.admin_routers import admin_router
from api.user.user_routers import user_router
from fastapi import APIRouter


mainRouter = APIRouter(
    prefix="/api/v1"
)


mainRouter.include_router(admin_router)
mainRouter.include_router(user_router)
