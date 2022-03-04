from dataclasses import dataclass
from app import app, db
import requests



MAPQUEST_API_KEY = "WTT4OcYoVpS0yFJqOcA4f9Wd1lWWXF3k"

# https://developer.mapquest.com/documentation/geocoding-api/address/get/
MAPQUEST_GEOCODING_URL = "http://open.mapquestapi.com/geocoding/v1/address"

# https://developer.mapquest.com/documentation/open/static-map-api/v4/map/get/
MAPQUEST_MAP_URL = "http://www.mapquestapi.com/staticmap/v4/getmap"


lat = float
lon = float
key = MAPQUEST_API_KEY
location = "Praha"
citiesToReturn = {}
url = "http://open.mapquestapi.com/geocoding/v1/address?key=" + key + "&location=" + location
res = requests.get(url)
data = res.json()
neco = data["results"][0]["locations"]
for i,elemI in enumerate(data["results"]):
    mesto= elemI["locations"][i]["adminArea5"] # ulozil jsem si z jsonu nazev mesta
    lat = elemI["locations"][i]["displayLatLng"]["lat"]
    lon = elemI["locations"][i]["displayLatLng"]["lng"]

    print(f"lon: {lon}, lat: {lat}" )


urlIm = "http://www.mapquestapi.com/staticmap/v4/getmap?key=" + key + "&size=600,400&zoom=13&center=" + str(lat)+","+str(lon)
size = (600,400)
resIm = requests.get(urlIm)

with open("mapa1.jpg","wb") as f:
    f.write(resIm.content)
#data = resIm.json()
print(resIm)
print(1)