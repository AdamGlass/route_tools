import os
import requests
from urllib.parse import quote


import polyline

from filters import regular_intervals

mapbox_url = 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{1}/auto/600x600?access_token={0}'


def get_static_map(image, overlays):

    quoted_overlays = ','.join(overlays)
    url = mapbox_url.format(os.environ['MAPBOX_TOKEN'], quoted_overlays)
    r = requests.get(url)
    if r.status_code == 200:
        with open(image, 'wb') as f:
            f.write(r.content)
    else:
        print(r.text)
    print(r)


def image_route_compare(intended_gpx, ridden_gpx, image):

    interval = 1
    while True:
        intended_points = [(p['lat'],p['lon']) for p in regular_intervals(intended_gpx.points_with_attributes(), interval)]
        ridden_points = [(p['lat'],p['lon']) for p in regular_intervals(ridden_gpx.points_with_attributes(), interval)]
        intended_polyline = polyline.encode(intended_points)
        ridden_polyline = polyline.encode(ridden_points)

        intended = quote('path-3+ff0000-0.5({0})'.format(intended_polyline))
        ridden = quote('path-3+0000ff-0.5({0})'.format(ridden_polyline))
        if len(intended) + len(ridden) > 7000:
            interval += 1
            continue
        else:
            break

    print(interval)
    start = quote('pin-l-bicycle+00ff00({0},{1})'.format(ridden_points[0][1], ridden_points[0][0]))
    end = quote('pin-s-bicycle+ff0000({0},{1})'.format(ridden_points[0][1], ridden_points[0][0]))
    get_static_map(image, [start, end, intended, ridden])

def image_route(gpx, image):

    points = [(p['lat'],p['lon']) for p in regular_intervals(gpx.points_with_attributes(), 1)]

    encoded_polyline = polyline.encode(points)
    start = quote('pin-l-bicycle+00ff00({0},{1})'.format(points[0][1], points[0][0]))
    end = quote('pin-s-bicycle+ff0000({0},{1})'.format(points[0][1], points[0][0]))
    path = quote('path-3+0000ff-0.5({0})'.format(encoded_polyline))
    get_static_map(image, [start, end, path])
