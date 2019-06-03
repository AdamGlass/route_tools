from scipy.spatial.distance import directed_hausdorff
import numpy as np

def similarity(intended_gpx, ridden_gpx):
    intended_points = [(p['lat'],p['lon']) for p in intended_gpx.points()]
    ridden_points = [(p['lat'],p['lon']) for p in ridden_gpx.points()]
    intended_set = set(intended_points)
    ridden_set = set(ridden_points)

    proto = {}
    proto['derivative'] = 1 - len(ridden_set - intended_set)/len(ridden_set)


    i = np.array(intended_points)
    r = np.array(ridden_points)

    x = directed_hausdorff(i, r)
    proto['hausdorff'] = x[0]
    return proto
