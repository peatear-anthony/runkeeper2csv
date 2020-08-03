import os
import datetime
import gpxpy
import gpxpy.gpx
import logging 
import logging.config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians
from statistics import mean


class Activity():
    '''
    This class will represent one activity. To initiate this class, we will need to provide it with the path to the gpx file.
    '''
    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(__name__)
        self.total_distance = None
        self.duration = None
        self.avg_pace = None
        self.date = None
        self.start_time = None
        self.end_time = None

        # Start private methods 
        self._load_gpx()
        self._segment_df = self._get_segment_df()
        self._get_activity_values()
        self._get_splits_df()
        '''
        self._segment_df.plot(x='t_cumsum', y='avg_pace')
        plt.show()
        '''

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
        e_list = []

        for segment in self.gpx.tracks[0].segments:
            t = [float((segment.points[i + 1].time - segment.points[i].time).seconds)
                for i in range(len(segment.points) - 1)]

            d = [self._calc_distance(segment.points[i + 1], segment.points[i]) 
                for i in range(len(segment.points) - 1)]

            e = [mean([segment.points[i + 1].elevation , segment.points[i].elevation])
                for i in range(len(segment.points) - 1)]

            t_list.extend(t)
            d_list.extend(d)
            e_list.extend(e)
            
        df = pd.DataFrame(zip(d_list, t_list, e_list), columns=['delta_d', 'delta_t', 'avg_elevation'])
        df = df.drop(df[df.delta_t > 15].index)
        df['pace'] = self._calc_pace(df['delta_d'], df['delta_t'])
        df['d_cumsum'] = df['delta_d'].cumsum()
        df['t_cumsum'] = df['delta_t'].cumsum()
        df['avg_pace'] = self._calc_pace(df['d_cumsum'], df['t_cumsum'])

        return df


    def _get_splits_df(self):
        # Calculate the splits for the activity then returns the results in a df
        indexes = [abs(self._segment_df['d_cumsum'] - km * 1e3).idxmin() 
        for km in range(1, int(self.total_distance / 1e3) + 1)]
        indexes.insert(0, 0)
                
        splits = [self._segment_df.iloc[indexes[i + 1]].t_cumsum -self._segment_df.iloc[indexes[i]].t_cumsum
                    for i in range(len(indexes) - 1)]
        splits = {float(km): str(datetime.timedelta(seconds=split)) 
                    for km, split in enumerate(splits, start=1)}

        # Add last split
        last_split = round((self._segment_df.iloc[-1].t_cumsum - self._segment_df.iloc[indexes[-1]].t_cumsum) \
            / (self.total_distance / 1e3 - len(splits)), 0)
        splits[round(self.total_distance/1e3, 1)] = str(datetime.timedelta(seconds=last_split))
        
        print(splits)
        return splits 


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
        return (1e3/(d/t))/60.0
    
    def _get_activity_values(self):
        # get the activity_values from the segment df
        self.total_distance = self._segment_df.tail(1)['d_cumsum'].values[0]
        self.duration = self._segment_df.tail(1)['t_cumsum'].values[0]
        self.avg_pace = str(datetime.timedelta(
            seconds = round(self._segment_df.tail(1)['avg_pace'].values[0] * 60)))
        self.start_time = self.gpx.tracks[0].segments[0].points[0].time
        self.end_time = self.gpx.tracks[0].segments[-1].points[-1].time

if __name__ == "__main__":
    logger_path = os.path.join(os.path.dirname(__file__), 'log', 'logging.conf')
    logging.config.fileConfig(logger_path)
    logger = logging.getLogger(__name__)

    file_path = os.path.join("data", "2020-07-26-183202.gpx")
    activity = Activity(file_path)


