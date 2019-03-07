import os
import requests
from urllib.parse import quote


import polyline

from filters import regular_intervals

mapbox_url = 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/path-5+f44-0.5({0})/auto/600x600?access_token=' + os.environ['MAPBOX_TOKEN']

def image_route(gpx, image):
    
    path = polyline.encode([(p['lat'],p['lon']) for p in regular_intervals(gpx.points_with_attributes(), 1)])
    print(mapbox_url.format(quote(path)))
    r = requests.get(mapbox_url.format(path))
    if r.status_code == 200:
        with open(image, 'wb') as f:
            f.write(r.content)
    else:
        print(r.text)
    print(r)
