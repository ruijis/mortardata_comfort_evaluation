"""Import packages for data engineering"""
import pandas as pd


def degree_hours(l, u, f):
    """
    Calculate the percentage of occupied time outside a temeprature range.
    The occupied time is supposed to be from 9 am to 5 pm at weekdays. 
    The data file type should be CSV.
    The first column of the CSV file should be time.
    The second column of the CSV file should be temperature.
    
    Parameters
    ----------
    l : float
        lower bound of the tempearture range, with same units of the data
    u : float
        upper bound of the temperature range, with same units of the data
    f : string
        file path of the csv dataset
    
    Returns
    ----------
    p : float
        percentage of the time
    """
    df = pd.read_csv(f)
    time = df.columns[0]
    temp = df.columns[1]
    # add a new column of weekdays
    df['wkdays'] = pd.to_datetime(df[time]).dt.dayofweek
    # calculate the interval (seconds) between two time stamps
    ts = pd.to_datetime(df[time][1]) - pd.to_datetime(df[time][0])
    ts_sec = ts.seconds
    # get rows that are out of the range
    df_out = df[(df[temp] < l) | (df[temp] > u)]
    out_sec = len(df_out)
    all_sec = len(df)
    
    