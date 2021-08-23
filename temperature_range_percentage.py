"""Import packages for data engineering"""
import pandas as pd
import glob

def temp_range(a, b, l, u, f):
    """
    Calculate the percentage of occupied time outside a temeprature range.
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
    f : string
        path of the fold that stores all CSV files

    Returns
    ----------
    p : float
        percentage of the time
    """
    path = glob.glob(f"{f}/*.csv")
    res_zone = []
    res_value = []
    for i in path:
        df = pd.read_csv(i)
        time = df.columns[0]
        temp = df.columns[1]
        df['hour'] = pd.to_datetime(df[time]).dt.hour
        df['weekdays'] = pd.to_datetime(df[time]).dt.dayofweek
        # create a new dataframe for the specified office hours and weekdays
        df_occ = df[(df['hour'] >= a) & (df['hour'] < b) &
                    (df['weekdays'] >= 0) & (df['weekdays'] <= 4)]
        # get rows from the new dataframe that are out of the temperature range
        df_out = df_occ[(df_occ[temp] < l) | (df_occ[temp] > u)]
        # Calculate the percentage of occupied time outside a temeprature range
        p = len(df_out) / len(df_occ)
        res_zone.append(i.partition(f)[2])
        res_value.append(p)
    res = pd.DataFrame({'zone name': res_zone, 'outside percentage': res_value})
    return res.sort_values(['outside percentage'], ascending=[False])  
    
    