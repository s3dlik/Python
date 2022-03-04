from dataclasses import dataclass
from app import app, db
import requests

from cv6Zadani.db import Centers

MAPQUEST_API_KEY = "WTT4OcYoVpS0yFJqOcA4f9Wd1lWWXF3k"

# https://developer.mapquest.com/documentation/geocoding-api/address/get/
MAPQUEST_GEOCODING_URL = "http://open.mapquestapi.com/geocoding/v1/address"

# https://developer.mapquest.com/documentation/open/static-map-api/v4/map/get/
MAPQUEST_MAP_URL = "http://www.mapquestapi.com/staticmap/v4/getmap"


@dataclass
class Location:
    lat: float
    lon: float


def get_location(location: str) -> Location:
    """
    TODO: download GPS (latitude, longitude) coordinates of the given location from MapQuest
    (see MAPQUEST_GEOCODING_URL)
    """
    url = "http://open.mapquestapi.com/geocoding/v1/address?key=" + MAPQUEST_API_KEY + "&location=" + location
    res = requests.get(url)
    data = res.json()
    for i, elemI in enumerate(data["results"]):
        mesto = elemI["locations"][i]["adminArea5"]  # ulozil jsem si z jsonu nazev mesta
        Location.lat = elemI["locations"][i]["displayLatLng"]["lat"] #ulozeni lat
        Location.lon = elemI["locations"][i]["displayLatLng"]["lng"] # ulozeni lng

    return Location



def get_map_image(location: Location) -> bytes:
    """
    TODO: download Map JPG image MapQuest (see MAPQUEST_MAP_URL)
    """
    urlIm = "http://www.mapquestapi.com/staticmap/v4/getmap?key=" + MAPQUEST_API_KEY + "&size=600,600&zoom=13&center=" + str(
        Location.lat) + "," + str(Location.lon)
    resIm = requests.get(urlIm)


    return resIm.content