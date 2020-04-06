
import pickle

import constants as const
# Various utilities used


def load_data():
    with open('countries.pkl', 'rb') as f:
        countries_dict = pickle.load(f)
    return countries_dict


def get_column_names(item):
    return const.plots[item]


def get_column_to_show(children):
    cols = []
    for child in children:
        if child['props']['active']:
            col = get_column_names(child['props']['id'])
            if "million" not in col:
                if 'poli' not in col:
                    cols.append(col)

    return cols


def get_date_from_index(date_index):
    with open('dates.pkl', 'rb') as f:
        dates = pickle.load(f)['confirmed_dates']
    date = dates[date_index]
    return date
