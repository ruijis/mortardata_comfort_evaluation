"""Import packages for data engineering"""
import pandas as pd
import glob

def temp_daily(a, b, p, f, e):
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
    p : float
        the precentile threshold of daily temperature range, eg. 0.8
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
    res_value = []
    res_threshold = []
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
        # calculate daily temperature range by max minus min
        df_max = df_occ.groupby(['date']).max()
        df_min = df_occ.groupby(['date']).min()
        df_range = df_max[temp] - df_min[temp]
        # get rows from the new dataframe that are out of the threshold
        t = df_range.quantile(p)
        df_out = df_range[(df_range > t)]
        # Calculate the percentage of occupied time outside the threshold
        p = len(df_out) / len(df_max)
        # store the zone name and percentage values for later sort
        res_zone.append(i.partition(f)[2])
        res_value.append(p)
        res_threshold.append(t)
        # export the dates that are out of the range
        df_out.rename("daily range").to_csv(f"{e}/{i.partition(f)[2]}")
    res = pd.DataFrame({'zone name': res_zone,
                        'outside percentage': res_value,
                        f'{p}percentile threshold': res_threshold})
    return res.sort_values(['outside percentage'], ascending=[False]) 


