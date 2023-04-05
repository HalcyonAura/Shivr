# GET /api/v1/maps/3413/pois.geojson/?h=20
# limit=2 # records
import json
import requests
import googlemaps

#shark_data= requests.get('https://www.mapotic.com/api/v1/maps/3413/pois.geojson/?h=20')
#print(x.text)


print("hello world")
data = None
with open('sharkdata.json', 'r') as f:
  data = json.load(f)

print(data)

for shark in data['features']:
  #print(shark['properties'])
  print("Name: " + shark['properties']['name'])
  print("Stage of Life: " +  shark['properties']['stage_of_life'])
  print("Gender: " +  shark['properties']['gender'])