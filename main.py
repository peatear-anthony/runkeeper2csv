import os
import gpxpy
import gpxpy.gpx
import logging 
import logging.config


if __name__ == "__main__":
    # Initate Logs
    logger_path = os.path.join(os.path.dirname(__file__), 'log', 'logging.conf')
    logging.config.fileConfig(logger_path)
    logger = logging.getLogger(__name__)

    file_path = os.path.join("data", "2020-07-07-190130.gpx")

    gpx_file = open(file_path, 'r')
    gpx = gpxpy.parse(gpx_file)


    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
                print(point.time)

