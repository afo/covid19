from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json


def get_data():
    import requests
    url = 'https://pomber.github.io/covid19/timeseries.json'
    countries = ['Sweden', 'Denmark', 'Norway', 'Finland', 'Iceland']
    df = pd.read_json(url)[countries]

    n_rows = df.shape[0]
    df['Sweden'][0]
    dates = []
    for i in range(n_rows):
        dates.append(df['Sweden'][i]['date'])

    df['Date'] = dates
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')

    df_deaths = pd.DataFrame(index=df.index)
    for col in df.columns:
        df_deaths[col] = [c.get('deaths') for c in df[col]]

    # Start from March 10 before first deaths
    df_deaths = df_deaths['2020-03-10':]
    # Fix faulty Iceland data
    df_deaths.loc['2020-03-15', 'Iceland'] = 0
    df_deaths.loc['2020-03-20', 'Iceland'] = 1

    df_pop = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)')[3]

    df_pop = df_pop[['Country or area', 'Population(1 July 2019)']]

    df_pop['Country or area'] = df_pop['Country or area'].str.replace(
        '\[.*\]', '')
    df_pop = df_pop.pivot_table(
        columns='Country or area', values='Population(1 July 2019)')[df.columns]
    df_pop = df_pop / 1000000
    df_deaths_per_mn = pd.DataFrame(index=df_deaths.index)

    for col in df_deaths.columns:
        df_deaths_per_mn[col] = df_deaths[col] / df_pop[col].values

    df_deaths_1 = df_deaths[df_deaths != 0]
    # Remove all dates with zero deaths
    df_deaths_1 = df_deaths_1.apply(lambda x: pd.Series(x.dropna().values))

    # Add zero to first day
    df_deaths_1 = pd.concat([pd.DataFrame(np.zeros((1, df_deaths_1.shape[1])),
                                          columns=df_deaths_1.columns), df_deaths_1], axis=0, ignore_index=True)

    # deaths per mn inhabitants since first death
    df_deaths_per_mn_1 = pd.DataFrame(index=df_deaths_1.index)
    for col in df_deaths.columns:
        df_deaths_per_mn_1[col] = df_deaths_1[col] / df_pop[col].values

    date = df_deaths.index[-1].to_pydatetime()+timedelta(days=1)
    obj = {'df_deaths': df_deaths.to_json(), 'df_deaths_per_mn': df_deaths_per_mn.to_json(),
           'df_deaths_1': df_deaths_1.to_json(), 'df_deaths_per_mn_1': df_deaths_per_mn_1.to_json(),
           'date': datetime.timestamp(date)}
    return json.dumps(obj)
