import pymortar
import pandas as pd

def daily_range_outlier(md, sd, ed, sh, eh, th):
    """
    Calculate the percentage of occupied days when temp range is outside the threshold.
    The occupied days is Monday to Friday but the occupied time can be specified.
    
    Parameters
    ----------
    md : str
         sensor metadata with prefix of http://buildsys.org/ontologies
    sd : str
         start date with format year-month-day, e.g.'2016-1-1'
    ed : str
         end date with format year-month-day, e.g.'2016-1-31'
    sh : int
         start hour of normal occupied time with 24-hour clock, e.g. 9
    eh : int
         end hour of normal occupied time with 24-hour clock, e.g. 17
    th : float
         threshold of daily temperature range, with default F unit
        
    Returns
    ----------
    p : float
        percentage of the time
    """
    assert isinstance(sd, str), 'The start date should be in a string.'
    assert isinstance(ed, str), 'The end date should be in a string.'
    assert sh < eh, "The start and end hour should be 24-hour clock."
    # connect client to Mortar frontend server
    client = pymortar.Client("https://beta-api.mortardata.org")
    data_sensor = client.data_uris([md])
    data = data_sensor.data
    # get a pandas dataframe between start date and end date of the data
    sd_ns = pd.to_datetime(sd, unit='ns', utc=True)
    ed_ns = pd.to_datetime(ed, unit='ns', utc=True)
    df = data[(data['time'] >= sd_ns) & (data['time'] <= ed_ns)]
    # parse the hour and weekday info and add it as a column
    df['hr'] = pd.to_datetime(df['time']).dt.hour
    df['wk'] = pd.to_datetime(df['time']).dt.dayofweek
    df['da'] = pd.to_datetime(df['time']).dt.date
    # create occupied df by normal office hours and by weekdays
    df_occ = df[(df['hr'] >= sh) & (df['hr'] < eh) &
                (df['wk'] >= 0) & (df['wk'] <= 4)]
    # calculate occupied daily temperature range by max minus min
    df_occ_max = df_occ.groupby(['da']).max()
    df_occ_min = df_occ.groupby(['da']).min()
    # add a new column to the df_max called range
    df_occ_max['range'] = df_occ_max['value'] - df_occ_min['value']
    # create a new df containing rows that are out of the threshold
    df_out = df_occ_max[(df_occ_max['range'] > th)]
    p = len(df_out) / len(df_occ) if len(df_occ) != 0 else 0
    return round(p, 2)