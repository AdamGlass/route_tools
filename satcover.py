from skyfield.api import Topos, Loader
from filters import regular_intervals

globalstar_url = 'http://celestrak.com/NORAD/elements/globalstar.txt'

def visible_satellites(sats, observer, t):
    def to_sky_position(sat):
        diff = sat - observer
        topocentric_diff = diff.at(t)
        return (topocentric_diff.altaz(), sat)

    sats_relative_position = map(to_sky_position, sats)
    visible_sats = filter(lambda x: x[0][0].degrees > 0, sats_relative_position)
    return list(visible_sats)

def satcover_route(parser):
    print('start satcover')
    load = Loader('/tmp/skyfield')
    planets = load('de421.bsp')
    print('start planets')
    ts = load.timescale()
    t = ts.now()
    print('start timescale')
    (globalstar_sat) = (load.tle(globalstar_url))
    print('load globastar')
    total_sat = len(globalstar_sat.values())

    earth = planets['earth']
    sat = globalstar_sat['GLOBALSTAR M036 [-]']

    for p in regular_intervals(parser.points_with_attributes(), 10):
        observer = Topos(latitude_degrees = float(p['lat']), longitude_degrees = float(p['lon']))
        x = visible_satellites(globalstar_sat.values(), observer, t)
        print(observer, len(x), total_sat)
