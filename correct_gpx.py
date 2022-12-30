from gpxpy.gpx import GPX

from read_gpx import get_gpx_points, parse_gpx_file

import gpxpy.gpx


def create_new_gpx():
    new_gpx = gpxpy.gpx.GPX()

    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    new_gpx.tracks.append(gpx_track)

    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    return new_gpx


# print(gpx.to_xml())
def save_gpx(file_name: str, gpx: GPX):
    with open(f'./data/{file_name}_gecorrigeerd.gpx', 'w') as f:
        f.write(gpx.to_xml())


def filter_points(gpx: GPX, cutoff_max_lat: float):
    new_gpx = create_new_gpx()
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if point.latitude < cutoff_max_lat:
                    new_gpx.tracks[0].segments[0].points.append(point)
    return new_gpx


def remove_points(file: str, cutoff_max_lat=52.01):
    gpx = parse_gpx_file(file_path)
    points = get_gpx_points(file)
    df = points[points['latitude'] < cutoff_max_lat]

    # Create points:
    for idx in df.index:
        gpx_segment.points.append(gpx.GPXTrackPoint(df.loc[idx, 0], df.loc[idx, 1]))

    print(df)


if __name__ == '__main__':
    gpx = parse_gpx_file('./data/Middagloop_12072022.gpx')
    filtered_gpx = filter_points(gpx, 52.01)
    save_gpx('Middagloop_12072022', filtered_gpx)
