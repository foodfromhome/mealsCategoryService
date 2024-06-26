from typing import List

from pydantic import BaseModel


class AddMealsSchema(BaseModel):
    mealName: str
    mealDescription: str
    mealPrice: float
    mealIngredients: List[str]

