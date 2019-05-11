import polyline
import requests

from filters import regular_intervals

router_url = 'https://router.project-osrm.org/match/v1/car/'

def mapmatch_route(gpx):
#    points = [(p['lat'],p['lon']) for p in regular_intervals(gpx.points_with_attributes(), 1)]
#    encoded_polyline = polyline.encode(points)
#    coordinates = 'polyline({0})'.format(encoded_polyline)
    points_str = ['{0},{1}'.format(p['lon'],p['lat']) for p in regular_intervals(gpx.points_with_attributes(), 10)]
    coordinates = ';'.join(points_str)

    params = {
        'overview': 'false',
        'steps': 'false',
        'geometries': 'polyline',
        'annotations': 'true'
   }
    url = router_url + coordinates + '?steps=true'
    r = requests.get(url, params=params)
    print(r.text)
