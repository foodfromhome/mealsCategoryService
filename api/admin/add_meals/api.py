from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from api.admin.add_meals.models import Meals, MealCategory
from api.admin.add_meals.config import s3_client

router = APIRouter()


@router.post("/add-meals", status_code=status.HTTP_201_CREATED, summary="Добавление блюд",
             response_model=Meals)
async def add_meals(name: str = Form(...),
                    description: str = Form(...),
                    price: float = Form(...),
                    category: MealCategory = Form(...),
                    ingredient: List[str] = Form(...),
                    images: List[UploadFile] = File(...)):
    try:
        meal = Meals(name=name, description=description, price=price, ingredient=ingredient, category=category)

        await meal.save()

        if images:

            for image in images:

                image.filename = image.filename.lower()

                file_key = await s3_client.upload_file(image, meal_id=meal.id, type='meals')
                meal.images.append(file_key)
            await meal.save()

        return meal

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))
