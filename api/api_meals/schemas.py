from datetime import datetime
from typing import Optional, List

from beanie import PydanticObjectId
from pydantic import BaseModel

from api.api_meals.models import MealCategory


class MealsSchemas(BaseModel):
    id: PydanticObjectId
    name: str
    description: str
    price: float
    category: MealCategory
    calories: Optional[int]
    serving_size: Optional[str]
    ingredients: Optional[List[str]]
    allergens: Optional[List[str]]
    preparation_time: Optional[int]
    rating: Optional[float]
    popularity: Optional[int]
    date_added: Optional[datetime]
    available: bool
    images: Optional[List[str]]
