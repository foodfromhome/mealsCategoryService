from beanie import Document, PydanticObjectId
from typing import Optional, List
from pydantic import Field
from datetime import datetime
from api.admin.add_meals.models.category import MealCategory


class Meals(Document):
    id: PydanticObjectId = Field(None, alias="_id")
    user_id: int = Field(None, alias="user_id")
    name: str = Field(None, alias="name")
    description: str = Field(None, alias="description")
    price: float = Field(..., gt=0, alias="price")
    category: MealCategory = Field(..., alias="category")
    calories: Optional[int] = Field(None, alias="calories")
    serving_size: Optional[str] = Field(None, alias="serving_size")
    ingredients: Optional[List[str]] = Field(None, alias="ingredients")
    allergens: Optional[List[str]] = Field(None, alias="allergens")
    preparation_time: Optional[int] = Field(None, alias="preparation_time")
    rating: Optional[float] = Field(None, alias="rating")
    popularity: Optional[int] = Field(None, alias="popularity")
    date_added: Optional[datetime] = Field(None, alias="date_added")
    available: bool = Field(True, alias="available")
    images: Optional[List[str]] = Field([], alias="images")

