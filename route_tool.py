import argparse
import json

import requests

from gpx import GpxParser
from places import place_route_data
from weather import weather_route_now
from satcover import satcover_route
from output import simple_output, geojson_output
from image import image_route, image_route_compare, image_save
from similarity import similarity
from stats import stats_route, stats_report
from mapmatch import mapmatch_route

def route_data(s):
    if s.startswith('http'):
        r = requests.get(s, stream=True)
        r.raise_for_status()
        return r.content
    else:
        return open(s, "rb")

parser = argparse.ArgumentParser(description='route tool')
group = parser.add_mutually_exclusive_group()
group.add_argument('--places', action='store_true')
group.add_argument('--weather', action='store_true')
group.add_argument('--satcover', action='store_true')
group.add_argument('--image', type=str)
group.add_argument('--stats', action='store_true')
group.add_argument('--image-compare', nargs=2, type=str, metavar=('OTHER-ROUTE', 'IMAGE'))
group.add_argument('--similarity', type=str, metavar=('OTHER-ROUTE'))
group.add_argument('--mapmatch', action='store_true')
parser.add_argument('route', type=str)
parser.add_argument('--place_interval', type=float, default=2.0)
parser.add_argument('--place_offroute', type=float, default=2.0)
parser.add_argument('--output', type=str, default='simple')

args = parser.parse_args()

gpxdata = route_data(args.route)

gpx = GpxParser(gpxdata)

weather_data = place_data = satcover_data = []

if args.places:
    place_data = place_route_data(gpx, args.place_interval, args.place_offroute)
    if args.output == 'simple':
        simple_output(gpx, place_data)
    else:
        geojson_output(gpx, place_data)

if args.weather:
    weather_data = weather_route_now(gpx)
    print(weather_data)

if args.satcover:
    satcover_data = satcover_route(gpx)

if args.image:
    image = image_route(gpx, args.image)
    image_save(image, args.image)

if args.image_compare:
    image = image_route_compare(gpx, GpxParser(route_data(args.image_compare[0])), args.image_compare[1])
    image_save(image, args.image_compare[1])

if args.similarity:
    data = similarity(gpx, GpxParser(route_data(args.similarity)))
    print(data)

if args.mapmatch:
    mapmatch_route(gpx)

if args.stats:
    data = stats_route(gpx)
    stats_report(data)
