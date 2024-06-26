from pydantic import BaseModel
from beanie import PydanticObjectId
from typing import Optional, List


class MealResponse(BaseModel):
    id: PydanticObjectId
    name: str
    description: str
    image: str


class ProfileResponse(BaseModel):
    first_name: str
    last_name: str
    image: str


class AdminResponseSchema(BaseModel):
    # admin_profile: ProfileResponse = None
    meals: Optional[List[MealResponse]]
