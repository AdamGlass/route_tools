import argparse
import json

import requests

from gpx import GpxParser
from places import place_route_data
from weather import weather_route_now
from output import simple_output, geojson_output

parser = argparse.ArgumentParser(description='route tool')
parser.add_argument('route', type=str)
parser.add_argument('--places', action='store_true')
parser.add_argument('--place_interval', type=float, default=2.0)
parser.add_argument('--place_offroute', type=float, default=2.0)
parser.add_argument('--weather', action='store_true')
parser.add_argument('--output', type=str, default='simple')

args = parser.parse_args()

if args.route.startswith('http'):
    r = requests.get(args.route, stream=True)
    r.raise_for_status()
    gpxdata = r.text
else:
    gpxdata = open(args.route, "r")

gpx = GpxParser(gpxdata)

if args.places:
    place_data = place_route_data(gpx, args.place_interval, args.place_offroute)
else:
    place_data = []

if args.weather:
    weather_data = weather_route_now(gpx)
else:
    weather_data = []

if args.output == 'simple':
    simple_output(gpx, place_data, weather_data)
elif args.output == 'geojson':
    geojson_output(gpx, place_data, weather_data)
