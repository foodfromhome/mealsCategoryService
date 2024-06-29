import json
import requests
from config import settings


async def get_info_from_edamam_api(ingredients):
    edamam_app_id = settings.edamam_app_id
    edamam_app_key = settings.edamam_app_key

    edamam_response = requests.get(
        f"https://api.edamam.com/api/food-database/v2/parser",
        params={
            "app_id": edamam_app_id,
            "app_key": edamam_app_key,
            "ingr": "%20".join(ingredients),
            "nutrition-type": "cooking"
        }
    )

    edamam_data = edamam_response.json()

    calories, allergens = extract_calories_and_allergens(edamam_data)

    return calories, allergens


def extract_calories_and_allergens(json_data):
    data = json_data
    parsed_data = data['parsed'][0]['food']
    calories = parsed_data['nutrients'].get('ENERC_KCAL', 0)
    allergens = []

    for ingredient in data['hints']:
        food = ingredient['food']
        if 'measures' in food:
            for measure in food['measures']:
                if 'Allergen' in measure['label']:
                    allergens.append(measure['label'].split(': ')[1])

    return calories, allergens
