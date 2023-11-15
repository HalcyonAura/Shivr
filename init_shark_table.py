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

# For every shark get attributes
for shark in shark_data['features']:  
  name = shark['properties']['name']

  # attributes
  stage_of_life = shark['properties']['stage_of_life'] # e.g. adult
  gender = shark['properties']['gender']
  length = shark['properties']['length']
  weight = shark['properties']['weight']

  # meta data
  last_update = shark['properties']['last_update'] # use zping_datetime? but only if zping is true
  species = shark['properties']['species'] #type, maybe rewrite to species
  image = shark['properties']['image'] # profile img link

  # write to db, is there a better way to mass write this?
  cur.execute('INSERT INTO sharks (name, age, gender, weight, length, type, image, last_online) VALUES (?,?,?,?,?,?,?,?)', 
              (name, stage_of_life, gender, weight, length, species, image, last_update))

# Confirm everything's written
#res = cur.execute('SELECT * from sharks').fetchall()
#print(len(res))
#for r in res:
#   print(r[1]) # print name of each record
connection.commit()
connection.close()