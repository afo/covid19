import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd
import pickle
import os
from flask import send_from_directory
from button_callbacks import button_callbacks

import layout
import constants as const
import utilities as utils
import figures

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = layout.generate_layout()
button_callbacks(app)

@app.callback(Output('deaths_plot', 'children'),
              [Input('country_selection', 'value'),
               Input('testing', 'children'),
               Input('picked-dates', 'start_date'),
               Input('picked-dates', 'end_date'),
               Input('log-scale', 'value'),
               Input('mobility_index', 'active'),
               Input('per_million', 'active'),
               Input('death', 'active'),
               Input('ICU', 'active'),
               Input('confirmed', 'active'),
               Input('political', 'active'),
               Input('since_first', 'active')
               ])
def update_total_deaths(countries, which_plots, start_date, end_date, scale, mobility, per_mn, check, check1, check2, political, since_first):
    # TODO(@Andreasfo@gmail.com)
    # Fix this callback inputs. It  triggers for everything
    # Sometimes multiple times in a row. Needs to  be fixed
    if not countries or not start_date or not end_date:
        return html.Div()
    if not which_plots:
        return html.Div()
    columns = utils.get_column_to_show(which_plots)
    if not columns:
        return html.Div()
    scale = next((s for s in scale), None)
    country_dicts = utils.load_data()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    data = {}
    # TODO(@Andreasfo@gmail.com)
    # Clean this upp, it is not readable at the moment
    # Drag it into a function instead this callback is  way to loong
    for country in countries:
        country_data = pd.DataFrame(columns=columns)
        for col in columns:
            if "ICU" in col and "Sweden" not in country:
                continue
            elif "mobility" in col:
                try:
                    country_feature = country_dicts[country][col].copy()
                except Exception as e:
                    continue
            else:
                if per_mn:
                    country_feature = country_dicts[country][col] / \
                        const.pops[country]
                else:
                    country_feature = country_dicts[country][col]
                if since_first:
                    country_feature = country_feature[country_feature > 0]
                    country_feature = country_feature.reset_index(drop=True)

            country_data[col] = country_feature

        if since_first:
            data[country] = country_data
        else:
            data[country] = country_data[(country_data.index >= start_date)
                                         & (country_data.index <= end_date)]

    if mobility:
        fig = figures.plot_graph_with_mobility(data, political, per_mn)
    else:

        fig = figures.plot_graph(data, political, per_mn, scale)
    fig.update_layout(height=600)
    return dcc.Graph(id="Plot", figure=fig)


@app.callback([Output('picked-dates', 'min_date_allowed'),
               Output('picked-dates', 'max_date_allowed'),
               Output('picked-dates', 'start_date'),
               Output('picked-dates', 'end_date')],
              [Input('data', 'children')])
def get_date_picker(json_obj):
    if not json:
        return None
    # TODO(andreasfo@gmail.com)
    # So we can se more into the past
    with open('dates.pkl', 'rb') as f:
        dates = pickle.load(f)['death_dates']
    min_date = dates[0]
    start_date = dates[37]
    end_date = dates[-1]
    return min_date, end_date + timedelta(days=1), start_date, end_date


@app.callback(Output('Map', 'children'),
              [Input('date-slider', 'value'),
               Input('map_total_cases', 'active'),
               Input('map_iva_patients', 'active'),
               Input('map_death', 'active'),
               Input('mobility_map', 'active')])
def plot_map(date_index, total, iva, death, mobility):
    fig = figures.plot_map(date_index, total, iva, death, mobility)
    map_graph = dcc.Graph(id="Map", figure=fig)
    return html.Div([map_graph])


STATIC_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static')

# Used for HTTP Health Check
@app.server.route('/static/<resource>')
def serve_static(resource):
    return send_from_directory(STATIC_PATH, resource)


if __name__ == "__main__":
    if os.environ['ENVIRONMENT'] == "dev":
        debugging = True
    else:
        debugging = False
    app.run_server(debug=debugging, host='0.0.0.0')
    pass
