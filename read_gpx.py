import gpxpy.gpx
import pandas as pd


def parse_gpx_file(file_path: str):
    """
    Parse gpx file using gpxpy.parse if file exists

    :param file_path: str, path to gpx file
    :return: gpxpy.GPX object
    """
    gpx = None
    try:
        with open(file_path, 'r') as file:
            gpx = gpxpy.parse(file)
    except FileNotFoundError as e:
        print(e)
    return gpx


def extract_points(gpx):
    """
    Loops through all points in gpx. Makes no distinction between tracks or segments; all points are saved into
    one list.
    For every point a dict is created with the latitude, longitude, elevation, timestamp, and index (by enumerate)
    of that point.

    :param gpx: gpx track, expected to have track(s), segment(s) and points
    :return: list of dicts, single dict per point
    """
    gpx_points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for index, point in enumerate(segment.points):
                gpx_points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'timestamp': str(point.time),
                    'index': index
                })
    return pd.DataFrame(gpx_points)


def get_gpx_points(file_path):
    """
    Parse GPX file and return a list of gpx points
    :param file_path: path to gpx file
    :return: list
    """
    gpx = parse_gpx_file(file_path)
    return extract_points(gpx)
