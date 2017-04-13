import argparse

from gpx import GpxParser
from places import place_route_data

import requests

parser = argparse.ArgumentParser(description='route tool')
parser.add_argument('route', type=str)
parser.add_argument('--places', action='store_true')
parser.add_argument('-interval', type=int, default=5)

args = parser.parse_args()

if args.route.startswith('http'):
    r = requests.get(args.route, stream=True)
    r.raise_for_status()
    gpxdata = r.text
else:
    gpxdata = open(args.route, "r")

gpx = GpxParser(gpxdata)

print (args)

if args.places:
    data = place_route_data(gpx)
    print(data)

    for d in data:
        print('{0}, {1}, {2}'.format(d.name, d.address, d.opening_hours_text))
