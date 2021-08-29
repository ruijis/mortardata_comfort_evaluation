"""Import packages for data engineering"""
import pandas as pd
import glob

def temp_degree(l, u, s, f):
    """
    Calculate the product sum of weighted factors and exposure time time.
    The data file type should be CSV.
    The first column of the CSV file should be time.
    The second column of the CSV file should be temperature.
    
    Parameters
    ----------
    a : int
        The start time (24-hour clock) of normal office hours during weekdays
    b : int
        The end time (24-hour clock) of normal office hours during weekdays
    l : float
        lower bound of the tempearture range, with same units of the data
    u : float
        upper bound of the temperature range, with same units of the data
    s : string
        the weighting factor calculation method, either ISO or EN
    f : string
        path of the fold that stores all CSV files


    Returns
    ----------
    p : float
        percentage of the time
    """
    df = pd.read_csv(f)
    time = df.columns[0]
    temp = df.columns[1]
    # get temperature data that are higher than the upper bound
    df_hot = df[(df[temp] > u)]
    df_hot_diff = df_hot[temp] - u
    # get temperature difference that are lower than the lower bound
    df_cold = df[(df[temp] < l)]
    df_cold_diff = l - df_cold[temp]
    # Calculate the percentage of occupied time outside a temeprature range
    p = (len(df_hot) + len(df_cold)) / len(df)
    return p