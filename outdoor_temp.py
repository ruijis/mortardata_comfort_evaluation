"""Import packages for querying dataset"""
import pymortar
import pandas as pd
import re

def hourly_outlier():

    # connect client to Mortar frontend server
    url  = "https://beta-api.mortardata.org"
    ct = pymortar.Client(url)
    # get the brick metadata of the query sensor at the specified site
    q =  """SELECT ?sensor ?equip WHERE {{
        ?sensor    rdf:type/rdfs:subClassOf*     brick:Zone_Air_Temperature_Sensor .
        ?sensor    brick:isPointOf ?equip .
    }}"""
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
    
    