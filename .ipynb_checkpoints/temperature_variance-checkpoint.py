"""Import packages for data engineering"""
import pandas as pd
import glob

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
        path of the fold that stores all CSV files
    
    Returns
    ----------
    v : float
        variance of occupied hourly average temperature data
    """
    path = glob.glob(f"{f}/*.csv")
    res_zone = []
    res_value = []
    for i in path:
        df = pd.read_csv(i)
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
        res_zone.append(i.partition(f)[2])
        res_value.append(v)
    res = pd.DataFrame({'zone name': res_zone, 'temperature vairance': res_value})
    return res.sort_values(['temperature vairance'], ascending=[False])  
    
    