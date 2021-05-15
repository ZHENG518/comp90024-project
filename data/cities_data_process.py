import json

with open('./cities.json', 'r') as f:
    data = json.load(f)

cities_data = {
    'crs': {
        "type": "name",
        "properties": {
            "name": "urn:x-ogc:def:crs:EPSG:4283"
        }
    },
    'type': 'FeatureCollection',
    'features':[]
}

for i in [0,2,4,14]:
    item = data['features'][i]
    item['properties'] = {'city_name': item['properties']['feature_name']}
    cities_data['features'].append(item)

with open('./cities_data.json', 'w') as f:
    json.dump(cities_data, f)

