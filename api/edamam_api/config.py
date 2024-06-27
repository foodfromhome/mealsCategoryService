import requests


def send_request_eda_mam():
    url = "https://api.edamam.com/api/food-database/v2/parser"


    params = {
        'app_id': '647ba147',
        'app_key': 'ffbb16c2483439e0209881142cb33678',
        'ingr': 'cooked rice',
        'nutrition-type': 'cooking'
    }

    response = requests.get(url, params=params, headers={'accept': 'application/json'})

    if response.status_code == 200:
        return response.json()
    else:
        return None


result = send_request_eda_mam()
if result:
    print(result)
