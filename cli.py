import json
import sys

from gpx import GpxParser
from filters import regular_intervals
from places import place_search, place_detail


with open('Haven_t_we_been_here__Fleche_2017.gpx') as f:
    parser = GpxParser(f)

    places = []
    for p in regular_intervals(parser.points_with_attributes(), 2.0):
        print(p, file=sys.stderr)
        if p['cum_distance'] < 200:
            continue
        new_places = list(place_search(p['lat'], p['lon'], 2.0, ['bicycle_store', 'bakery', 'cafe', 'convenience_store', 'grocery_or_supermarket', 'food']))
        places.extend(new_places)

    unique_places = set(places)
    places = map(place_detail, unique_places)
    for p in places:
        hours = p.get('opening_hours')
        if hours:
            hours = p['opening_hours'].get('weekday_text')
        else:
            hours = 'UNKNOWN'
        print('{0}\t{1}\t{2}'.format(p['name'], p['formatted_address'], hours, p['types']))
