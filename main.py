import argparse
import os
import glob
import logging 
import logging.config
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from activity import Activity


if __name__ == "__main__":
    # Initate Logs
    logger_path = os.path.join(os.path.dirname(__file__), 'log', 'logging.conf')
    logging.config.fileConfig(logger_path)
    logger = logging.getLogger(__name__)

    # Arg Parser stuff
    parser = argparse.ArgumentParser(description="Convert gpx data to csv files")
    parser.add_argument("-s", "--summary", action="store_true",
        help="Get summary CSV")
    parser.add_argument("-a", "--activity", action="store_true",
        help="Get CSV for every activity")

    args = parser.parse_args()

    # Define raw .gpx directory path
    directory_path = os.path.join("data")

    # Today's date (Filename)
    today = datetime.date.today()
    filename = today.strftime("%Y-%m-%d") + '.csv'

    total_distance = []
    duration = []
    avg_pace = []
    date = []
    start_time = []
    end_time = []

    for filepath in glob.glob(os.path.join(directory_path, '*.gpx')):
        activity = Activity(filepath)
        total_distance.append(activity.total_distance)
        duration.append(activity.duration)
        avg_pace.append(activity.avg_pace)
        date.append(activity.date)
        start_time.append(activity.start_time)
        end_time.append(activity.end_time)

        if args.activity:
            # Splits to csv
            splits = activity.get_splits_df()
            activity_df = pd.DataFrame(splits.items(), columns=['km', 'duration'])
            fname = activity.date.strftime("%Y-%m-%d") + '.csv'
            save_path = os.path.join('csv', 'activity', 'splits', fname)
            activity_df.to_csv(save_path)

            # Segment df to csv
            save_path = os.path.join('csv', 'activity', 'segment', fname)
            activity._segment_df.to_csv(save_path)

    if args.summary:
        df = pd.DataFrame(zip(date, total_distance, duration, avg_pace, start_time, end_time), 
            columns=['date', 'total_distance', 'duration', 'avg_pace', 'start_time', 'end_time'])
        save_path = os.path.join('csv', 'summary', filename)
        df.to_csv(save_path)



