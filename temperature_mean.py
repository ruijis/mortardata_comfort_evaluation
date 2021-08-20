"""Import packages for data engineering"""
import pandas as pd


def temp_mean(a, b, f):
    """
    Calculate mean value of the temperature at occupied time.
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
    m : float
        mean value of the tempearture
    """
    df = pd.read_csv(f)
    time = df.columns[0]
    temp = df.columns[1]
    df['hour'] = pd.to_datetime(df[time]).dt.hour
    df['weekdays'] = pd.to_datetime(df[time]).dt.dayofweek
    # create a new dataframe for the specified office hours and weekdays
    df_occ = df[(df['hour'] >= a) & (df['hour'] < b) &
                (df['weekdays'] >= 0) & (df['weekdays'] <= 4)]
    # Calculate mean value of the temperature from the new datafram
    m = df_occ[df_occ.columns[1]].mean()
    return m
    
    