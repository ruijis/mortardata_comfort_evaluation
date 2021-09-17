"""Import packages for data engineering"""
import pandas as pd
import glob
import matplotlib.pyplot as plt

def daily_range_outlier(a, b, t, f, e):
    """
    Calculate the percentage of occupied time whose range is outside the threshold.
    The data file type should be CSV.
    The first column of the CSV file should be time.
    The second column of the CSV file should be temperature.
    
    Parameters
    ----------
    a : int
        The start time (24-hour clock) of normal office hours during weekdays
    b : int
        The end time (24-hour clock) of normal office hours during weekdays
    t : float
        the precentile threshold of all measure daily temperature range, eg. 0.8
    f : string
        path of the folder that stores inporting CSV files
    e : string
        path of the folder that stores exporting CSV files
        
    Returns
    ----------
    p : float
        percentage of the time
    """
    path = glob.glob(f"{f}/*.csv")
    res_zone = []
    res_threshold = []
    res_percentage = []
    for i in path:
        df = pd.read_csv(i)
        # rename the column name
        df.columns = ['datetime', 'temp']
        # get the date from the time for groupby function later on
        df['date'] = pd.to_datetime(df['datetime']).dt.date
        df['hour'] = pd.to_datetime(df['datetime']).dt.hour
        df['weekdays'] = pd.to_datetime(df['datetime']).dt.dayofweek
        # calculate the percetile threshold value by all daily tempearture range
        df_max = df.groupby(['date']).max()
        df_min = df.groupby(['date']).min()
        df_max['range'] = df_max['temp'] - df_min['temp']
        t_value = df_max['range'].quantile(t)
        # occupied dataframe for the specified office hours and weekdays
        df_occ = df[(df['hour'] >= a) & (df['hour'] < b) &
                    (df['weekdays'] >= 0) & (df['weekdays'] <= 4)]
        # calculate occupied daily temperature range by max minus min
        df_occ_max = df_occ.groupby(['date']).max()
        df_occ_min = df_occ.groupby(['date']).min()
        # add a new column to the df_max called range
        df_occ_max['range'] = df_occ_max['temp'] - df_occ_min['temp']
        # create a new df containing rows that are out of the threshold
        df_out = df_occ_max[(df_occ_max['range'] > t_value)]
        p = len(df_out) / len(df_occ)
        # plot the weekday frequency
        plt.figure()
        df_out['weekdays'].plot.hist()
        # store the zone name and percentage values for later sort
        res_zone.append(i.partition(f)[2])
        res_threshold.append(t_value)
        res_percentage.append(p)
        # export the dates that are out of the range
        df_out.to_csv(f"{e}/{i.partition(f)[2]}")
    res = pd.DataFrame({'zone name': res_zone,
                        f'{t}percentile threshold': res_threshold,
                        'outlier percentage': res_percentage})
    return res.sort_values(['outlier percentage'], ascending=[False]) 


