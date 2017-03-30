from gpx import GpxParser
from filters import regular_intervals

with open('SIR_Permanent_1845__Flat_Snohomish-Edison_200K.gpx') as f:
    parser = GpxParser(f)
    for p in regular_intervals(parser.points_with_attributes(), 10.0):
        print(p)
