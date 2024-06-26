from fastapi import APIRouter, HTTPException
from api.models_init import Meals
from typing import List
from api.user.user_main.schemas import MealsResponse
from starlette import status
from starlette.responses import JSONResponse
from beanie import PydanticObjectId

router = APIRouter()


@router.get("/main", summary="Главная страница", status_code=status.HTTP_200_OK,
            response_model=List[MealsResponse])
async def main():
    try:

        data = await Meals.find().to_list()

        return data

    except HTTPException as e:
        JSONResponse(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/main/{meals_id}", summary="Достать блюдо по id", status_code=status.HTTP_200_OK,
            response_model=Meals)
async def get_meals_id(meals_id: PydanticObjectId):
    try:

        meal = await Meals.get(meals_id)

        if not meal:

            return JSONResponse(content="Meal not found", status_code=status.HTTP_404_NOT_FOUND)

        return meal

    except HTTPException as e:
        JSONResponse(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
