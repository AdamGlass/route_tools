
def similarity(intended_gpx, ridden_gpx):
    intended_points = [(p['lat'],p['lon']) for p in intended_gpx.points()]
    ridden_points = [(p['lat'],p['lon']) for p in ridden_gpx.points()]
    intended_set = set(intended_points)
    ridden_set = set(ridden_points)

    proto = {}
    proto['derivative'] = 1 - len(ridden_set - intended_set)/len(ridden_set)
    return proto
