from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from api.api_meals.models import Meals, MealCategory
from api.api_meals.config import s3_client
from api.api_meals.schemas import MealsSchemas
from beanie import PydanticObjectId

router = APIRouter()


@router.post("/{user_id}/meals", status_code=status.HTTP_201_CREATED, summary="Добавление блюд",
             response_model=Meals)
async def add_meals(user_id: int,
                    name: str = Form(...),
                    description: str = Form(...),
                    price: float = Form(...),
                    category: MealCategory = Form(...),
                    ingredient: List[str] = Form(...),
                    images: List[UploadFile] = File(...)):
    try:
        meal = Meals(name=name,
                     description=description,
                     price=price,
                     ingredient=ingredient,
                     category=category,
                     chefs_id=user_id)

        await meal.save()

        if images:

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
async def get_meals_for_id(chefs_id: int, meals_id: PydanticObjectId):
    try:

        meals = await Meals.get(meals_id)

        if not meals:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meals not found")

        return meals

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))


@router.put("/meals/{meals_id}", status_code=status.HTTP_200_OK,
            summary="Обновляет блюдо по id")
async def update_meals_for_id(meals_id: PydanticObjectId,
                              name: str = Form(None),
                              description: str = Form(None),
                              price: float = Form(None),
                              category: MealCategory = Form(None),
                              ingredient: List[str] = Form(None),
                              images: List[UploadFile] = File(None)):
    try:

        meals = await Meals.get(meals_id)

        if not meals:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meals not found")

        meals.name = name
        meals.description = description
        meals.price = price
        meals.category = category
        meals.ingredient = ingredient

        if images:
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
            response_model=List[MealsSchemas])
async def get_all_meals():
    try:

        meals = await Meals.find().to_list()

        return meals

    except HTTPException as e:

        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))