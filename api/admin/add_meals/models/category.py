from pydantic import BaseModel
from enum import Enum


class MealCategory(str, Enum):
    appetizers = "Закуски"
    salads = "Салаты"
    soups = "Супы"
    main_courses = "Основные блюда"
    garnishes = "Гарниры"
    desserts = "Десерты"
    beverages = "Напитки"
    sauces_and_condiments = "Соусы и приправы"
    baking = "Выпечка"
    grilled_dishes = "Блюда на гриле"
