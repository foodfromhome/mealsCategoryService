from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from .schemas import AdminResponseSchema


router = APIRouter()


@router.get('/admin-main', summary="Главная страница повара", status_code=status.HTTP_200_OK,
            response_model=AdminResponseSchema)
async def admin_main():
    try:

        pass

    except HTTPException as e:
        return JSONResponse(content=str(e), status_code=status.HTTP_400_BAD_REQUEST)
