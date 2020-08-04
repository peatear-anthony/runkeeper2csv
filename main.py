import os
import glob
import logging 
import logging.config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from activity import Activity



if __name__ == "__main__":
    # Initate Logs
    logger_path = os.path.join(os.path.dirname(__file__), 'log', 'logging.conf')
    logging.config.fileConfig(logger_path)
    logger = logging.getLogger(__name__)

    directory_path = os.path.join("data")

    total_distance = []
    duration = []
    avg_pace = []
    date = []
    start_time = []
    end_time = []

    for filepath in glob.glob(os.path.join(directory_path, '*.gpx')):
        logger.info(filepath)
        activity = Activity(filepath)
        total_distance.append(activity.total_distance)
        duration.append(activity.duration)
        avg_pace.append(activity.avg_pace)
        date.append(activity.date)
        start_time.append(activity.start_time)
        end_time.append(activity.end_time)

    df = pd.DataFrame(zip(date, total_distance, duration, avg_pace, start_time, end_time), 
        columns=['date', 'total_distance', 'duration', 'avg_pace', 'start_time', 'end_time'])
    df.plot(x='total_distance', y='avg_pace', kind='scatter')
    plt.show()




