import json
import sys

from gpx import GpxParser
from filters import regular_intervals
from places import place_search, place_detail


with open('Haven_t_we_been_here__Fleche_2017.gpx') as f:
    parser = GpxParser(f)
