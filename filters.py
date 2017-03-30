
def regular_intervals(points, interval):
    cum_distance = 0.0
    first = True
    for p in points:
        if first:
            yield p
            first = False
        else:
            cum_distance += p['distance']
        last_p = p
        if cum_distance >= interval:
            yield p
            cum_distance = 0.0
    yield last_p
