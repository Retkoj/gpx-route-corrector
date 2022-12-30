import gpxpy.gpx
import pandas as pd


def parse_gpx_file(file_path: str):
    gpx = None
    try:
        with open(file_path, 'r') as file:
            gpx = gpxpy.parse(file)
    except FileNotFoundError as e:
        print(e)
    return gpx


def extract_points(gpx):
    gpx_points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                gpx_points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'timestamp': point.time
                })
    return pd.DataFrame(gpx_points)


def get_gpx_points(file_path):
    gpx = parse_gpx_file(file_path)
    return extract_points(gpx)
#
# for waypoint in gpx.waypoints:
#     print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))
#
# for route in gpx.routes:
#     print('Route:')
#     for point in route.points:
#         print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))



