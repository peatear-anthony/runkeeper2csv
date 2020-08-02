import os
import gpxpy
import gpxpy.gpx
import logging 
import logging.config
import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians


class Activity():
    '''
    This class will represent one activity. To initiate this class, we will need to provide it with the path to the gpx file.
    '''
    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(__name__)
        # Start private methods 
        self._load_gpx()
        self._segment_df = self._get_segment_df()
        print(self._segment_df)
        self._segment_df.plot(x='t_cumsum', y='avg_pace')
        plt.show()
    
    def _load_gpx(self):
        #  Load gpx file from path
        if self.path.split('.')[-1] != 'gpx':
            self.logger.error('%s: Path to file does not have gpx extentsion.', self.path)
            raise NameError('Wrong file extentsion')
        else:
            self.logger.debug("Loading gpx file from path %s", self.path)
            gpx_file = open(self.path, 'r')
            self.gpx = gpxpy.parse(gpx_file)

    def _get_segment_df(self):
        # Return dataframe with activity information
        t_list = []
        d_list = []
        for segment in self.gpx.tracks[0].segments:
            t = [float((segment.points[i + 1].time - segment.points[i].time).seconds)
                for i in range(len(segment.points) - 1)]

            d = [self._calc_distance(segment.points[i + 1], segment.points[i]) 
                for i in range(len(segment.points) - 1)]
            
            t_list.extend(t)
            d_list.extend(d)

        df = pd.DataFrame(zip(d_list, t_list), columns=['delta_d', 'delta_t'])
        df = df.drop(df[df.delta_t > 6].index)
        df['pace'] = self._calc_pace(df['delta_d'], df['delta_t'])
        df['d_cumsum'] = df['delta_d'].cumsum()
        df['t_cumsum'] = df['delta_t'].cumsum()
        df['avg_pace'] = self._calc_pace(df['d_cumsum'], df['t_cumsum'])


        return df


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

        return R*c

    def _calc_pace(self, d, t):
        # Given d and t will return the pace in min/km
        return (1000/(d/t))/60.0

if __name__ == "__main__":
    logger_path = os.path.join(os.path.dirname(__file__), 'log', 'logging.conf')
    logging.config.fileConfig(logger_path)
    logger = logging.getLogger(__name__)

    file_path = os.path.join("data", "2020-07-07-190130.gpx")
    activity = Activity(file_path)

