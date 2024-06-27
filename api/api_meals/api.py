import logging
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from api.api_meals.models import Meals, MealCategory
from api.api_meals.schemas import MealsSchemas
from beanie import PydanticObjectId
from fastapi_cache.decorator import cache


from api.s3.main import s3_client

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/{user_id}/meals", status_code=status.HTTP_201_CREATED, summary="Добавление блюд",
             response_model=Meals)
async def add_meals(user_id: int,
                    name: str = Form(...),
                    description: str = Form(...),
                    price: float = Form(...),
                    category: MealCategory = Form(...),
                    ingredient: List[str] = Form(...),
                    images: Optional[List[UploadFile]] = File(None)):
    try:
        meal = Meals(name=name,
                     description=description,
                     price=price,
                     ingredient=ingredient,
                     category=category,
                     user_id=user_id)

        await meal.save()

        if images is not None:

            for image in images:
                image.filename = image.filename.lower()

                file_key = await s3_client.upload_file(image, meal_id=meal.id, type='api_meals')
                meal.images.append(file_key)
            await meal.save()
        return meal

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))


@router.get("/meals/{meals_id}", status_code=status.HTTP_200_OK,
            summary="Возвращает блюдо по id", response_model=MealsSchemas)
@cache(expire=120)
async def get_meals_for_id(meals_id: PydanticObjectId):
    logger.info(f"Fetching meal {meals_id} from cache or database")
    try:

        meals = await Meals.get(meals_id)

        if not meals:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meals not found")

        return meals

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))


@router.put("/meals/{meals_id}", status_code=status.HTTP_200_OK,
            summary="Обновляет блюдо по id", response_model=MealsSchemas)
async def update_meals_for_id(meals_id: PydanticObjectId,
                              name: Optional[str] = Form(None),
                              description: Optional[str] = Form(None),
                              price: Optional[float] = Form(None),
                              category: Optional[MealCategory] = Form(None),
                              ingredients: Optional[List[str]] = Form(None),
                              images: Optional[List[UploadFile]] = File(None)):
    try:

        meals = await Meals.get(meals_id)

        if not meals:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meals not found")

        if name is not None:
            meals.name = name
        if description is not None:
            meals.description = description
        if price is not None:
            meals.price = price
        if category is not None:
            meals.category = category
        if ingredients is not None:
            meals.ingredients = ingredients

        if images is not None:
            for image in images:
                image.filename = image.filename.lower()

                file_key = await s3_client.upload_file(image, meal_id=meals.id, type='api_meals')
                meals.images.append(file_key)

        await meals.save()

        return meals

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))


@router.delete("/meals/{meals_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удаление блюдо по id")
async def delete_meals_for_id(meals_id: PydanticObjectId):
    try:

        meals = await Meals.get(meals_id)

        if not meals:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meals not found")

        await meals.delete()

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))


@router.get("/meals", status_code=status.HTTP_200_OK, summary="Возвращает все блюда",
            response_model=Optional[List[MealsSchemas]])
@cache(expire=120)
async def get_all_meals():
    logger.info("Fetching all meals from cache or database")
    try:

        meals = await Meals.find().to_list()

        if meals:

            return meals

        return []

    except HTTPException as e:

        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))
