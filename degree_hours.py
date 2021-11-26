import pymortar
import pandas as pd

def degree_hours(md, sd, ed, sh, eh, sl, su, wl, wu):
    """
    Calculate the product sum of weighted factors and exposure time time.

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
    sl : float
         lower bound of the tempearture range in summer, with default F unit
    su : float
         upper bound of the temperature range in summer, with default F unit
    wl : float
         lower bound of the tempearture range in winter, with default F unit
    wu : float
         upper bound of the temperature range in winter, with default F unit

    Returns
    ----------
    ps : float
         degree hours
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
    df['mo'] = pd.to_datetime(df['time']).dt.month
    # create occupied df by normal office hours and by weekdays
    df_occ = df[(df['hr'] >= sh) & (df['hr'] < eh) &
                (df['wk'] >= 0) & (df['wk'] <= 4)]
    # split the occupied data to the summer and  winter
    df_occ_sum = df_occ[(df_occ['mo'] >= 5) & (df_occ['mo'] <= 10)]
    df_occ_win = df_occ[(df_occ['mo'] >= 11) | (df_occ['mo'] <= 4)]
    # overheating and overcooling rows in summer and winter
    df_sum_oc = df_occ_sum[(df_occ_sum['value'] < sl)]
    df_sum_oh = df_occ_sum[(df_occ_sum['value'] > su)]
    df_win_oc = df_occ_win[(df_occ_win['value'] < wl)]
    df_win_oh = df_occ_win[(df_occ_win['value'] > wu)]
    # magnitude of overheating and overcooling in summer and winter
    sum_oc_diff = (sl - df_sum_oc['value']).sum()
    sum_oh_diff = (df_sum_oh['value'] - su).sum()
    win_oc_diff = (wl - df_win_oc['value']).sum()
    win_oh_diff = (df_win_oh['value'] - wu).sum()
    # sum and then multiple one hour
    ps = (sum_oc_diff + sum_oh_diff + win_oc_diff + win_oh_diff) * (15/60)
    return round(ps, 2)