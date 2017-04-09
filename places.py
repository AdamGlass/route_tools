import requests
import time
import os

place_search_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
place_detail_url = 'https://maps.googleapis.com/maps/api/place/details/json'

def place_search_core(lat, lng, radius, type):
    place_params = {
        'key': os.environ['GOOGLE_PLACES_KEY'],
        'location': '{0}, {1}'.format(lat, lng),
        'radius': radius * 1000,
        'type': type
    }

    while True:
        r = requests.get(place_search_url, params=place_params)
        places = r.json()
        for p in places['results']:
            yield p['place_id']
        if 'next_page_token' in places:
            place_params['pagetoken'] = places['next_page_token']
        else:
            break

def place_search(lat, lng, radius, types):
    for t in types:
        yield from place_search_core(lat, lng, radius, t)

def place_detail(id):
    place_params = {
        'key': os.environ['GOOGLE_PLACES_KEY'],
        'placeid': id
    }
    
    r = requests.get(place_detail_url, params=place_params)
    return r.json()['result']
