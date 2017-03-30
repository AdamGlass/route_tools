from gpx import GpxParser
from filters import regular_intervals
from places import place_search, place_detail

with open('SIR_Permanent_1845__Flat_Snohomish-Edison_200K.gpx') as f:
    parser = GpxParser(f)
    for p in regular_intervals(parser.points_with_attributes(), 10.0):
        print(p)
        for place in place_search(p['lat'], p['lon'], 'coffee'):
            detail = place_detail(place[1])
            print('\t{0}'.format(detail['name']))
