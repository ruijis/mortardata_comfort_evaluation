"""Import packages for querying dataset"""
import pymortar
import pandas as pd
import re

def hourly_outlier(q, s, a, b, c, d, l, u):
    """
    Calculate the percentage of normal occupied time outside a specified temeprature range.
    The normal occupied days is Monday to Friday but the occupied time can be specified.
    
    Parameters
    ----------
    q : str
        sparql query using brick metadata schema
    s : str
        single qualied site name, using abbreviation
    a : str
        start date with format year-month-day, e.g.'2016-1-1'
    b : str
        end date with format year-month-day, e.g.'2016-1-31'
    c : int
        start hour of normal occupied time with 24-hour clock, e.g. 9
    d : int
        end hour of normal occupied time with 24-hour clock, e.g. 17
    l : float
        lower bound of the tempearture range, with default F unit
    u : float
        upper bound of the temperature range, with default F unit

    Returns
    ----------
    p : float
        percentage of the time
    """
    assert isinstance(a, str), 'The start date should be in a string.'
    assert isinstance(b, str), 'The end date should be in a string.'
    assert c < d, "The start and end hour should be 24-hour clock."

    # connect client to Mortar frontend server
    url  = "https://beta-api.mortardata.org"
    ct = pymortar.Client(url)
    # get the brick metadata of the query sensor at the specified site
    meta = ct.sparql(q, sites=[s])
    zone = []
    res = []
    for id in meta.sensor:
        # get dataset using the ontology url as id
        q_res = ct.data_uris([id])
        data = q_res.data
        # get a pandas dataframe between start date and end date of the data
        a = pd.to_datetime(a, unit='ns', utc=True)
        b = pd.to_datetime(b, unit='ns', utc=True)
        df = data[(data['time'] >= a) & (data['time'] <= b)]
        # parse the hour and weekday info and add it as a column
        df['hr'] = pd.to_datetime(df['time']).dt.hour
        df['wk'] = pd.to_datetime(df['time']).dt.dayofweek
        # get rows that among the specified office hours during weekdays
        df_occ = df[(df['hr'] >= c) & (df['hr'] < d) &
                    (df['wk'] >= 0) & (df['wk'] <= 4)]
        # get rows that are out of the temperature range
        df_out = df_occ[(df_occ['value'] < l) | (df_occ['value'] > u)]
        # Calculate the percentage of occupied time outside the temeprature range
        p = len(df_out) / len(df_occ)
        id_zone = re.split('[.]', id)[-2]
        zone.append(id_zone)
        res.append(p)
    df_res = pd.DataFrame({'zone': zone, 'hourly_outlier percentage': res})
    df_sort = df_res.sort_values(['hourly_outlier percentage'], ascending=[False])
    return  df_sort
    
    