import time
import os
import sys
from collections import namedtuple

import requests

from filters import regular_intervals

place_search_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
place_detail_url = 'https://maps.googleapis.com/maps/api/place/details/json'

PlaceData = namedtuple('placedata', 'name address opening_hours_text opening_hours types coord')

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


def place_route_data(parser, interval, offroute):
    places = []
    for p in regular_intervals(parser.points_with_attributes(), interval):
        print(p, file=sys.stderr)
        new_places = list(place_search(p['lat'], p['lon'], offroute, ['bicycle_store', 'bakery', 'cafe', 'convenience_store', 'grocery_or_supermarket', 'food', 'campground', 'lodging', 'gas_station']))
        places.extend(new_places)

    unique_places = set(places)
    for place in unique_places:
        p = place_detail(place)
        hours = p.get('opening_hours')
        if hours:
            hours = p['opening_hours'].get('weekday_text')
        else:
            hours = 'UNKNOWN'
        yield PlaceData(p['name'], p['formatted_address'], hours, p.get('periods'), p['types'], (p['geometry']['location']['lng'], p['geometry']['location']['lat']))
