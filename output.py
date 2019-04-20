from geojson import LineString, Feature, FeatureCollection, Point
import geojson

def simple_output(parser, place_data):
    for d in place_data:
        print('{0}, {1}, {2}'.format(d.name, d.address, d.opening_hours_text))

def geojson_output(parser, place_data):
    features = []
    route = LineString(list(map(lambda p: (p['lon'], p['lat']), parser.points())))
    route_feature = Feature(geometry=route)
    features.append(route_feature)

    places = list(map(lambda p: Feature(geometry=Point(p.coord),properties=p._asdict()), place_data))
    features.extend(places)

    collection = FeatureCollection(features)
    dump = geojson.dumps(collection, sort_keys=True, indent=4)
    print(dump)
