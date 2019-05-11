from datetime import timedelta
import arrow

def stats_route(gpx):
    points = [p for p in gpx.points_with_attributes()]
    point_count = len(points)
    distance = points[-1]['cum_distance']
    if points[0].get('time'):
        start_time = arrow.get(points[0]['time']).datetime
        end_time = arrow.get(points[-1]['time']).datetime
    else:
        start_time = None
        end_time = None

    if start_time:

        last_moved = start_time
        moving_time = timedelta()
        for i in range(1,len(points)):
            point_time = arrow.get(points[i]['time']).datetime
            if points[i]['distance'] >= 0.0005:
                moving_time += point_time - last_moved
            last_moved = point_time

        duration = end_time - start_time

    print('Points   : {0}'.format(point_count))
    print('Distance : {0:.3f}'.format(distance))
    print('Start    : {0}'.format(start_time))
    print('End      : {0}'.format(end_time))
    if start_time and end_time:
        print('Duration : {0}'.format(duration))
        print('Moving   : {0}'.format(moving_time))
