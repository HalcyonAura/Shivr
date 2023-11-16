# GET /api/v1/maps/3413/pois.geojson/?h=20
# limit=2 # records
import json
import sqlite3
import requests
#import googlemaps

# Connect to sqlite db, creates file if DNE
connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Get sharks endpoint
data = requests.get(
   'https://www.mapotic.com/api/v1/maps/3413/pois.geojson/?h=20')
shark_data = json.loads(data.text)
# Template data/test data retrieval
#data = None
#with open('.\static\sharkdata.json', 'r') as f:
#  data = json.load(f)

bios = None
with open('.\\static\\bios.json', 'r') as f:
  bios = json.load(f)

# For every shark get attributes
for shark in shark_data['features']:
  id = shark['properties']['id']
  slug = shark['properties']['slug']
  name = shark['properties']['name']

  # attributes
  stage_of_life = shark['properties']['stage_of_life'] # e.g. adult
  gender = shark['properties']['gender']
  length = shark['properties']['length']
  weight = shark['properties']['weight']
  species = shark['properties']['species'] #type, maybe rewrite to species

  # meta data
  last_update = shark['properties']['last_update'] # use zping_datetime? but only if zping is true
  image = shark['properties']['image'] # profile img link
  # under the assumption that coordinates will always be point objects in geometry obj
  lat = shark['geometry']['coordinates'][0]
  long = shark['geometry']['coordinates'][1]

  # write to db, is there a better way to mass write this?
  if slug in bios:
    cur.execute('INSERT INTO sharks (id, slug, name, age, gender, weight, length, species, image, last_online, bio, lat, long) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', 
              (id, slug,name, stage_of_life, gender, weight, length, species, image, last_update, bios[slug], lat, long))
  else:
    cur.execute('INSERT INTO sharks (id, slug, name, age, gender, weight, length, species, image, last_online, lat, long) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', 
              (id, slug,name, stage_of_life, gender, weight, length, species, image, last_update, lat, long))

# Confirm everything's written
#res = cur.execute('SELECT * from sharks').fetchall()
#print(len(res))
#for r in res:
#   print(r[1]) # print name of each record

# Confirm bios written
res = cur.execute('SELECT * from sharks where bio is not null').fetchall()
for r in res:
  print(r)
connection.commit()
connection.close()