import pymortar
import pandas as pd

def temp_var(md, sd, ed, sh, eh):
    """
    Calculate variance of occupied hourly average temperature data.
    
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
    
    Returns
    ----------
    v : float
        variance of occupied hourly average temperature data
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
    # get hourly average data by grouping by date frist and hour, then mean
    df_hrs = df_occ.groupby(['da', 'hr']).mean()
    # calculate variance of occupied hourly average temperature data.
    v = df_hrs['value'].var()
    return round(v, 2)