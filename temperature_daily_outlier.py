"""Import packages for data engineering"""
import pandas as pd


def temp_daily(a, b, t, f):
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
        the threshold of daily temperature range
    f : string
        file path of the CSV dataset
        
    Returns
    ----------
    p : float
        percentage of the time
    """
    df = pd.read_csv(f)
    time = df.columns[0]
    temp = df.columns[1]
    # get the date from the time for groupby function later on
    df['date'] = pd.to_datetime(df[time]).dt.date
    df['hour'] = pd.to_datetime(df[time]).dt.hour
    df['weekdays'] = pd.to_datetime(df[time]).dt.dayofweek
    # create a new dataframe for the specified office hours and weekdays
    df_occ = df[(df['hour'] >= a) & (df['hour'] < b) &
                (df['weekdays'] >= 0) & (df['weekdays'] <= 4)]
    # calculate daily temperature range
    # might need calculate max and min seperately
    df_max = df_occ.groupby(['date']).max()
    df_min = df_occ.groupby(['date']).min()
    df_range = df_max[temp] - df_min[temp]
    # get rows from the new dataframe that are out of the threshold
    df_out = df_range[(df_range > t)]
    # Calculate the percentage of occupied time outside the threshold
    p = len(df_out) / len(df_max)
    return p


