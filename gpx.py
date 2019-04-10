from io import StringIO

from lxml import etree as ET
from geopy.distance import great_circle as distance

ns = { 'gpx1': 'http://www.topografix.com/GPX/1/0',
       'gpx2': 'http://www.topografix.com/GPX/1/1'
}

class GpxParser():
    def __init__(self, source, **kwargs):
        try:
            str = source.read()
        except:
            str = source
        self.root = ET.XML(str)

    def points(self):
        for t in self.root.findall('./trk/trkseg/trkpt', self.root.nsmap):
            proto = {}
            proto['lat'] = float(t.attrib['lat'])
            proto['lon'] = float(t.attrib['lon'])

            for x in t.findall('./time', self.root.nsmap):
                proto['time'] = x.text

            yield proto

    def points_with_attributes(self):
        first = True
        cum_distance = 0.0
        for p in self.points():
            p_tuple = p['lat'], p['lon']
            if first:
                last_p = p_tuple
                first = False
            p_distance = distance(last_p, p_tuple).km
            last_p = p_tuple
            p['distance'] = p_distance
            cum_distance += p_distance
            p['cum_distance'] = cum_distance
            yield p
