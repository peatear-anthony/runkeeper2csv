import os
import gpxpy
import gpxpy.gpx
import logging 
import logging.config
from math import sin, cos, sqrt, atan2, radians


class Activity():
    '''
    This class will represent one activity. To initiate this class, we will need to provide it with the path to the gpx file.
    '''
    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(__name__)
        self._load_gpx()
        self._get_list()
    
    def _load_gpx(self):
        #  Load gpx file from path
        if self.path.split('.')[-1] != 'gpx':
            self.logger.error('%s: Path to file does not have gpx extentsion.', self.path)
            raise NameError('Wrong file extentsion')
        else:
            self.logger.debug("Loading gpx file from path %s", self.path)
            gpx_file = open(self.path, 'r')
            self.gpx = gpxpy.parse(gpx_file)

    def _get_list(self):
        # Fix bug were time is greater than 5 seconds (No count), case b/w breaks
        for segment in self.gpx.tracks[0].segments:
            for c1, c2 in zip(segment.points[0::2], segment.points[1::2]):
                d, t = self._calc_distance(c1, c2)
                if d:
                    pace = (1000/(d/t.seconds))/60.0
                else: 
                    pace = 0
                
                if t.seconds<5: print("Ran with pace {:.2f}, for {:.2f} meters, in {:.2f} seconds".format(pace, d, t.seconds))
                

    def _calc_distance(self, c1, c2):
        # Return delta-distance and delta-time between two coordinates.
        R = 6373000 # Radius of the earth in meters
        lat1 = radians(c1.latitude)
        lon1 = radians(c1.longitude)
        lat2 = radians(c2.latitude)
        lon2 = radians(c2.longitude)
        d_lon = lon2 - lon1
        d_lat = lat2 - lat1

        a = sin(d_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(d_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R*c, c2.time - c1.time


if __name__ == "__main__":
    logger_path = os.path.join(os.path.dirname(__file__), 'log', 'logging.conf')
    logging.config.fileConfig(logger_path)
    logger = logging.getLogger(__name__)

    file_path = os.path.join("data", "2020-07-29-201703.gpx")
    activity = Activity(file_path)

