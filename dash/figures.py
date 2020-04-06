import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import pandas as pd
import numpy as np

import utilities as utils
import constants as const


def plot_map(date_index, total, iva, death, mobility):
    """Generates the map in the dashboard

    TODO(@AndreasFO@gmail.com)
    callbacks do no work currently.
    Needs to be inspected
    Arguments:
        date_index {int} -- index of the date used (from slider)
        total {Boolean} -- If to visualize: Confirmed cases
        iva {Boolean} -- If to visualize: Intensive care
        death {Boolean} -- If to visualize: Deaths
        mobility {Boolean} -- If to visualize: Mobility

    Returns:
        Plotly Figure
    """
    date = utils.get_date_from_index(date_index)
    column = "Deaths"
    if total:
        column = "Tested_Confirmed"
    if death:
        column = "Deaths"
    if iva:
        column = "ICU_Patients"
    if mobility:
        column = "Mobility"
    from urllib.request import urlopen
    # Example data
    with open('data/features.geojson') as response:
        counties = json.load(response)
    df = pd.read_csv('data/map_data.csv')
    fig = px.choropleth_mapbox(df, geojson=counties, color=column,
                               locations="id",
                               center={'lat': 62.598584, 'lon': 12.961619},
                               mapbox_style="carto-positron", zoom=4, hover_name='NAME_1',
                               hover_data=['Deaths', 'Mobility',
                                           'Tested_Confirmed', 'ICU_Patients'],
                               color_continuous_scale=plotly.colors.diverging.RdYlGn[::-1],
                               #labels={'id':'Unique ID'},
                               category_orders={'id': None})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(hovermode="closest", width=800, height=700)
    return fig


def plot_graph_with_mobility(data, politics, per_mn, scale="linear"):
    """Generates a plot with mobility data on a second yaxis

    Arguments:
        data {dictionary} -- containing dataframes for each country
        politics {Boolean} -- If political decision is going to be shown
        per_mn {Boolean} -- Show per million inhabitants

    Keyword Arguments:
        scale {str} -- which scale to use (default: {"linear"})

    Returns:
        Plotly Figure
    """
    titley = ''
    if per_mn:
        titley = "Number of people per Million"
    else:
        titley = "Number of People"
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    max_val = 0
    for country, df in data.items():
        for col in df.columns:
            if 'mobility' not in col:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[col], name=country+' '+const.legends[col],
                    line={'dash': const.lines[col], 'color': const.colors[country]},),
                    secondary_y=True)
            else:
                if max_val < df[col].max():
                    max_val = df[col].max()
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[col], name="Mobility " + country, fill='tozeroy',
                    fillcolor=const.fillcolors[country], line={'color': const.colors[country], 'dash': 'dot'}),
                    secondary_y=False
                )

    fig.update_layout(template="plotly_white", title_text="Covid 19 Analysis",
                      xaxis_title="Dates",
                      hovermode='x',
                      xaxis_rangeslider_visible=False)
    fig.update_yaxes(title_text="Mobility %",
                     secondary_y=False)

    fig.update_yaxes(title_text=titley, secondary_y=True)
    if politics:
        fig = add_political_decision(fig, max_val)

    return fig


def plot_graph(data, politics, per_mn, scale='linear'):
    """Generates a plot with data predetermined on the dashboard

    Arguments:
        data {dictionary} -- containing dataframes for each country
        politics {Boolean} -- If political decision is going to be shown
        per_mn {Boolean} -- Show per million inhabitants

    Keyword Arguments:
        scale {str} -- which scale to use (default: {"linear"})

    Returns:
        Plotly Figure
    """
    titley = ''
    if per_mn:
        titley = "Number of peopler per Million"
    else:
        titley = "Number of People"
    fig = go.Figure()
    max_val = 0
    for country, df in data.items():
        for col in df.columns:
            if max_val < df[col].max():
                max_val = df[col].max()
            fig.add_trace(go.Scatter(
                x=df.index, y=df[col], name=country+' '+const.legends[col],
                line={'dash': const.lines[col], 'color': const.colors[country]}))

    fig.update_layout(template="plotly_white", title_text="Covid 19 Analysis",
                      xaxis_title="Dates",
                      yaxis_title=titley, yaxis=dict(fixedrange=True),
                      hovermode='x',
                      xaxis_rangeslider_visible=False)
    if scale == 'on':
        fig.update_layout(yaxis_type='log', yaxis_exponentformat="power")
    if politics:
        fig = add_political_decision(fig, max_val)

    return fig


def add_political_decision(fig, max_val):
    """Adds political decisions to a plotly figure  

    Arguments:
        fig {Plotly figure} -- figure to add decision to
        max_val {float} -- Where  to set the politics decision on y-axis

    Returns:
        Plotly Figure
    """
    df_dec = pd.read_csv('data/decisions.csv')
    df_dec['Date'] = pd.to_datetime(df_dec['Date'], yearfirst=True)
    df_dec = df_dec.set_index('Date')
    fig.add_trace(go.Scatter(
        x=df_dec.index,
        marker_symbol='x-dot',
        marker_line_color="black",
        marker_line_width=2, marker_size=10,
        y=np.repeat(max_val, df_dec.shape[0]),
        mode="markers",
        text=df_dec['Event'],
        hoverinfo="text",
        hoverlabel=dict(bgcolor='rgba(7, 164, 181, 0.5)'),
        marker=dict(color=px.colors.sequential.RdBu[-2]), name='Swedish Political Decisions'))

    fig.update_layout(
        shapes=[dict(
            type="line",
            x0=date,
            y0=0,
            x1=date,
            y1=max_val,
            line=dict(
                color="RoyalBlue",
                width=2
            )
        ) for date in df_dec.index])
    return fig
