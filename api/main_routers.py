from api.admin.admin_routers import router as admin_router
from fastapi import APIRouter


mainRouter = APIRouter()


mainRouter.include_router(admin_router)
