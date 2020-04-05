import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
import pickle


def get_data():
    """
    Downloads and cleans  data that is used for the covid19 dashboard
    Data is collected from:
        - Confirmed and Deaths (up until the last day)
            https://pomber.github.io/covid19/timeseries.json
        - Population
            https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)
        - Mobility index:
            https://www.data.gouv.fr/en/datasets/r/0e56f0f4-6a82-48d4-b677-96e950100176
        - Confirmed  and Deaths (Today)
            https://www.worldometers.info/coronavirus/

    Other datasets such as ICU patients are gathered daily from 
        https://portal.icuregswe.org/siri/report/inrapp-corona


    """
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

#    df = df.rename(columns={'US':'United States','Korea, South':'South Korea', 'Czechia':'Czech Republic'})

    df_deaths = pd.DataFrame(index=df.index)

    for col in df.columns:
        df_deaths[col] = [c.get('deaths') for c in df[col]]

    latest_data = death_update(countries)
    df_deaths = pd.concat([df_deaths, latest_data])
    # Start from March 10 before first deaths
    df_deaths = df_deaths[datetime(2020, 3, 8):]
    # Fix faulty Iceland data
    df_deaths.loc[datetime(2020, 3, 15, 0, 0, 0), 'Iceland'] = 0
    df_deaths.loc[datetime(2020, 3, 20, 0, 0, 0,), 'Iceland'] = 1
    df_confirmed = pd.DataFrame(index=df.index)
    for col in df.columns:
        df_confirmed[col] = [c.get('confirmed') for c in df[col]]
    latest_data = confirm_update(countries)

    df_confirmed = pd.concat([df_confirmed, latest_data])

    df_pop = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)')[3]

    df_pop = df_pop[['Country or area', 'Population(1 July 2019)']]

    df_pop['Country or area'] = df_pop['Country or area'].str.replace(
        '\[.*\]', '')
    df_pop = df_pop.pivot_table(
        columns='Country or area', values='Population(1 July 2019)')[df.columns]
    df_pop = df_pop / 1000000

    df_deaths_per_mn = pd.DataFrame(index=df_deaths.index)

    df_confirmed_per_mn = pd.DataFrame(index=df_confirmed.index)

    for col in df_deaths.columns:
        df_deaths_per_mn[col] = df_deaths[col] / df_pop[col].values

    for col in df_confirmed.columns:
        df_confirmed_per_mn[col] = df_confirmed[col] / df_pop[col].values

    # Fix later on so that each item is stored inside country_df directly
    obj = {'df_deaths': df_deaths, 'df_deaths_per_mn': df_deaths_per_mn}
    country_dict = {}
    for country in countries:
        country_df = pd.DataFrame()
        for k, df in obj.items():
            if '1' in k:
                continue
            else:
                country_df[k] = df[country]
        country_df['Cases'] = df_confirmed[country]
        country_df['Cases_per_mn'] = df_confirmed_per_mn[country]
        country_dict[country] = country_df

    mobility_url = "https://www.data.gouv.fr/en/datasets/r/0e56f0f4-6a82-48d4-b677-96e950100176"
    mobility_cities = {'Sweden': 'Stockholm', 'Denmark': 'Copenhagen'}
    for coun, ci in mobility_cities.items():
        mobility = get_mobility(ci)
        country_df = country_dict[coun]
        country_df['mobility'] = mobility
        country_dict[coun] = country_df

    # icu data, sweden only right now
    icu = pd.read_csv('data/swe_icu.csv')
    icu.index = pd.to_datetime(icu['Date'])
    swe = country_dict['Sweden']
    swe['ICU'] = icu['total_icu']
    country_dict['Sweden'] = swe

    with open('dates.pkl', 'wb') as f:
        dates = {'death_dates': df_deaths.index,
                 'confirmed_dates': df_confirmed.index}
        pickle.dump(dates, f)
    with open('countries.pkl', 'wb') as f:
        pickle.dump(country_dict, f)


def death_update(country=None):
    """Gets the latest status updatedeath of the corona Virus

    Keyword Arguments:
        country {List or string]} -- Countries/Country to extract data from (default: {None})

    Returns:
        Pandas DataFrame -- Latest update of covid19
    """
    url = 'https://www.worldometers.info/coronavirus/'
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    dfs = pd.read_html(r.text)
    df = dfs[0]
    df = df[['Country,Other', 'TotalDeaths']]
    df.columns = ['Date', 'Deaths']
    df = df.transpose()
    df.columns = df.loc['Date']
    df = df.drop('Date')
    df.index = [datetime.now().date()]
    df.set_index
    if country:
        return(df[country])
    else:
        return df


def confirm_update(country=None):
    """Gets the latest status update of confimred cases

    Keyword Arguments:
        country {List or string]} -- Countries/Country to extract data from (default: {None})

    Returns:
        Pandas DataFrame -- Latest update of covid19
    """
    url = 'https://www.worldometers.info/coronavirus/'
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    dfs = pd.read_html(r.text)
    df = dfs[0]
    df = df[['Country,Other', 'TotalCases']]
    df.columns = ['Date', 'Confirmed']
    df = df.transpose()
    df.columns = df.loc['Date']
    df = df.drop('Date')
    df.index = [datetime.now().date()]
    df.set_index
    if country:
        return(df[country])
    else:
        return df


def get_mobility(city):
    """Gets the latest mobility  data from city mapper

    Arguments:
        city {String} -- Which city to get data from

    Returns:
        Pandas Series -- Series of mobility index 
    """
    mobility = pd.read_csv(
        "https://www.data.gouv.fr/en/datasets/r/0e56f0f4-6a82-48d4-b677-96e950100176")
    mobility['date'] = pd.to_datetime(mobility['date'])
    city = mobility[mobility['city'] == city].copy()
    city.index = city['date']
    city['mobility'] = city['percentage']
    city = city.drop(['date', 'city', 'percentage'], axis=1)
    return city
