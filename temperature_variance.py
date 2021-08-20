"""Import packages for data engineering"""
import pandas as pd


def temp_var(a, b, f):
    """
    Calculate variance of occupied hourly average temperature data.
    The data file type should be CSV.
    The first column of the CSV file should be time.
    The second column of the CSV file should be temperature.
    
    Parameters
    ----------
    a : int
        The start time (24-hour clock) of normal office hours during weekdays
    b : int
        The end time (24-hour clock) of normal office hours during weekdays
    f : string
        file path of the CSV dataset
    
    Returns
    ----------
    v : float
        variance of occupied hourly average temperature data
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
    # get hourly average data by grouping by date frist and hour, then mean
    df_hrs = df_occ.groupby(['date', 'hour']).mean()
    # calculate variance of occupied hourly average temperature data.
    v = df_hrs[temp].var()
    return v
    
    