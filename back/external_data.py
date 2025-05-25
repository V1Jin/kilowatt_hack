import sys
import requests
from dadata import Dadata
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')

API_2GIS = "f93a5b47-6e3b-4c23-ba03-185daa02ef64"
API_DADATA = "8a4cfc00823055a56808d387105d4fc05bd8dd07"
SECRET_DADATA = "e140f92bdbb6098c1fab7d28cf5326b55916dca5"


def geocode_to_coords(api_key, text):
    url = f"https://catalog.api.2gis.com/3.0/items/geocode?q={text}&key={api_key}&fields=items.point"
    response = requests.get(url).json()
    return response["result"]["items"][0]["point"]

def geocode_to_id(api_key, text):
    url = f"https://catalog.api.2gis.com/3.0/items/geocode?q={text}&key={api_key}&fields=items.point"
    response = requests.get(url).json()
    return response["result"]["items"][0]["id"]


def point_to_url(location):
    loc_str = f"{location['lon']},{location['lat']}"
    return quote(loc_str)


def get_count_business(api_key, id): #количество организаций в здании
    url = f"https://catalog.api.2gis.com/3.0/items?building_id={id}&key={api_key}"
    try:
        response = requests.get(url).json()
        return len(response["result"]["items"])
    except KeyError:
        return 0


def get_has_business(api_key, id): #флаг, есть ли хоть один юрлицо на точке.
    url = f"https://catalog.api.2gis.com/3.0/items?building_id={id}&key={api_key}"
    try:
        response = requests.get(url).json()
        return len(response["result"]["items"]) > 0
    except KeyError:
        return False


def get_cadastral_number(text):
    dadata = Dadata(API_DADATA, SECRET_DADATA)
    result = dadata.clean("address", text)
    return result["house_cadnum"]

    
def get_property_type(kad_number):
    url = f"https://ns2.mapbaza.ru/api/geoportal/v2/search/geoportal?query={kad_number}"
    response = requests.get(url)
    data = response.json()
    try:
        return data["data"]["features"][0]["properties"]["options"]["purpose"]
    except (KeyError, TypeError):
        return None

text = "Краснодар Ставрапольская 149"
id = geocode_to_id(API_2GIS, text)
# print(point_to_url(geocode_to_coords(API_2GIS, "Западная 8 Тимашевск")))
print(text)
print("Кадастровый номер:",get_cadastral_number(text))
print("Тип:",get_property_type(get_cadastral_number(text)))
print("Есть ли бизнесы поблизости:", get_has_business(API_2GIS, id))
print("Количество организааций в здании:",get_count_business(API_2GIS, id))