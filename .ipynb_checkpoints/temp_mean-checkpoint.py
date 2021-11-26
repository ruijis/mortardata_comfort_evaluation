import pymortar
import pandas as pd

def temp_mean(md, sd, ed, sh, eh):
    """
    Calculate mean value of the temperature at occupied time.
    
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
    m : float
        mean value of the tempearture
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
    # create occupied df by normal office hours and by weekdays
    df_occ = df[(df['hr'] >= sh) & (df['hr'] < eh) &
                (df['wk'] >= 0) & (df['wk'] <= 4)]
    # Calculate mean value of the temperature from the new datafram
    m = df_occ['value'].mean()
    return round(m, 2)
    