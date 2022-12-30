from pathlib import Path

from gpxpy.gpx import GPX, GPXTrack, GPXTrackSegment

from read_gpx import parse_gpx_file


def create_new_gpx():
    """
    Create a gps track with a single segment without points

    :return: empty gpx track
    """
    new_gpx = GPX()

    # Create first track in our GPX:
    gpx_track = GPXTrack()
    new_gpx.tracks.append(gpx_track)

    # Create first segment in our GPX track:
    gpx_segment = GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    return new_gpx


def save_gpx(file_path, gpx: GPX, file_extension='corrected'):
    """
    Save gpx into a new gpx file, with new file name = old filename_{file_extension}, under folder {file_extension} in
    the original file directory. Directory is created if it doesn't exist.

    :param file_path: str, path to original gpx file
    :param gpx: gpx track to be saved
    :param file_extension: term to add to file name and what to call folder into which file is saved
    """
    (Path(file_path).parent / file_extension).mkdir(parents=True, exist_ok=True)
    path = (Path(file_path).parent / file_extension)
    file_name = Path(file_path).stem
    with open(path / f'{file_name}_{file_extension}.gpx', 'w') as f:
        f.write(gpx.to_xml())


def filter_points(gpx: GPX, exclude_lower_bound, exclude_upper_bound):
    """
    filter out points between lower and upper bound (inclusive, based on enumerate index)

    :param gpx: gpx track, expected to have track(s), segment(s) and points
    :param exclude_lower_bound: int, lowerbound index to remove
    :param exclude_upper_bound: int, upperbound index to remove
    :return: new gpx track
    """
    new_gpx = create_new_gpx()
    for track in gpx.tracks:
        for segment in track.segments:
            for index, point in enumerate(segment.points):
                # If point not in exluding bounds, add point
                if index < exclude_lower_bound or index > exclude_upper_bound:
                    new_gpx.tracks[0].segments[0].points.append(point)
    return new_gpx


def old_gpx_to_new(file_path):
    """
    Old Suunto device uses routes, without segments.
    this function saves the route points into a new gpx file with one track and one segment.
    New files are saved into subfolder 'gpx_formats'

    :param file_path: Path to gpx file
    """
    gpx = parse_gpx_file(file_path)
    new_gpx = create_new_gpx()
    for route in gpx.routes:
        for point in route.points:
            new_gpx.tracks[0].segments[0].points.append(point)
    save_gpx(file_path, new_gpx, file_extension='gpx_format')


def correct_gpx_file(file_path, exclude_lower_bound, exclude_upper_bound):
    """
    Parse gpx file, filter out points between lower and upper bound (inclusive, based on enumerate index),
    save new gpx file into subfolder 'corrected'.

    :param file_path: Path to GPX file
    :param exclude_lower_bound: int, lowerbound index to remove
    :param exclude_upper_bound: int, upperbound index to remove
    """
    gpx = parse_gpx_file(file_path)
    filtered_gpx = filter_points(gpx, exclude_lower_bound, exclude_upper_bound)
    save_gpx(file_path, filtered_gpx)
