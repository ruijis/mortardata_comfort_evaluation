"""Import packages for data engineering"""
import pandas as pd


def temp_range(l, u, f):
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
        file path of the CSV dataset
    
    Returns
    ----------
    p : float
        percentage of the time
    """
    df = pd.read_csv(f)
    time = df.columns[0]
    temp = df.columns[1]
    df['hour'] = pd.to_datetime(df[time]).dt.hour
    df['weekdays'] = pd.to_datetime(df[time]).dt.dayofweek
    # create a new occupied dataframe from 9 am to 5 pm at weekdays
    df_occ = df[(df['hour'] >= 9) & (df['hour'] < 17) &
                (df['weekdays'] >= 0) & (df['weekdays'] <= 4)]
    # get rows from the new dataframe that are out of the temperature range
    df_out = df_occ[(df_occ[temp] < l) | (df_occ[temp] > u)]
    # Calculate the percentage of occupied time outside a temeprature range
    p = len(df_out) / len(df_occ)
    return p
    
    