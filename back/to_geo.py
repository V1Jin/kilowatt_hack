import json
from external_data import geocode_to_coords

API_2GIS = "f93a5b47-6e3b-4c23-ba03-185daa02ef64"

with open('data_point.json', 'r', encoding='utf-8') as f:
    input_data = json.load(f)

# Преобразование в GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}

for item in input_data:
    coordinates = geocode_to_coords(API_2GIS,item["address"])
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [coordinates["lon"], coordinates["lat"]]
        },
        "properties": {
            "accountId": item["accountId"],
            "isCommercial": item["isCommercial"],
            "address": item["address"],
            "buildingType": item["buildingType"],
        }
    }
    
    geojson["features"].append(feature)

with open('output.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, indent=2, ensure_ascii=False)

print("результат сохранён в output.geojson")