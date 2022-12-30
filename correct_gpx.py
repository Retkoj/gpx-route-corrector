from pathlib import Path

from gpxpy.gpx import GPX

from read_gpx import parse_gpx_file

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


def save_gpx(file_name: str, gpx: GPX):
    Path('./data/corrected/').mkdir(parents=True, exist_ok=True)
    with open(f'./data/corrected/{file_name}_gecorrigeerd.gpx', 'w') as f:
        f.write(gpx.to_xml())


def filter_points(gpx: GPX, exclude_lower_bound, exclude_upper_bound):
    new_gpx = create_new_gpx()
    for track in gpx.tracks:
        for segment in track.segments:
            for index, point in enumerate(segment.points):
                # If point not in exluding bounds, add point
                if index < exclude_lower_bound or index > exclude_upper_bound:
                    new_gpx.tracks[0].segments[0].points.append(point)
    return new_gpx


def correct_gpx_file(file_path, exclude_lower_bound, exclude_upper_bound):
    file_name = Path(file_path).stem
    gpx = parse_gpx_file(file_path)
    filtered_gpx = filter_points(gpx, exclude_lower_bound, exclude_upper_bound)
    save_gpx(file_name, filtered_gpx)

