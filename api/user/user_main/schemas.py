from pydantic import BaseModel
from typing import List, Optional
from beanie import PydanticObjectId


class MealsResponse(BaseModel):
    id: PydanticObjectId
    name: str
    description: str
    images: Optional[List[str]] = []
