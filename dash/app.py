import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime, timedelta
import json
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle

import layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
tmp = dbc.themes.BOOTSTRAP
with open("check.txt", 'w') as f:
    f.writelines(tmp)

server = app.server

app.layout = layout.generate_layout()


def load_data():
    with open('countries.pkl', 'rb') as f:
        countries_dict = pickle.load(f)
    return countries_dict


dfs = ['df_deaths', 'df_deaths_per_mn', 'df_deaths_1', 'df_deaths_per_mn_1']
plots = {'death': 'df_deaths',
         'confirmed': 'Cases',
         'ICU': 'ICU',
         'mobility_index': 'mobility',
         'per_million': 'million',
         'political': 'politics'}
countries = ['Sweden', 'Finland', 'Denmark', 'Norway', 'Iceland']
active_map = ["map_death", 'map_total_cases',
              'map_iva_patients', 'mobility_map']
titles = {'df_deaths': 'COVID19 Total Nordic Deaths, starting March 10 2020',
          'df_deaths_per_mn': 'COVID19 Total Nordic Deaths per Mn inhabitants, starting March 10 2020',
          'df_deaths_1': 'COVID19 Total Nordic Deaths, daily data since first death',
          'df_deaths_per_mn_1': 'COVID19 Total Nordic Deaths per Mn inhabitants, daily data since first death'}
x_axis_labels = {'df_deaths': 'Date',
                 'df_deaths_per_mn': 'Date',
                 'df_deaths_1': 'Days since first Death',
                 'df_deaths_per_mn_1': 'Days since first Death'}
y_axis_labels = {'df_deaths': 'Deaths',
                 'df_deaths_per_mn': 'Deaths per Mn inhabitants',
                 'df_deaths_1': 'Deaths',
                 'df_deaths_per_mn_1': 'Deaths per Mn inhabitants'}

legends = {'df_deaths': 'Deaths',
           'Cases': 'Confirmed Cases',
           'ICU': 'Intensive Care',
           'mobility': 'Mobility ', }
colors = {'Sweden': 'blue',
          'Denmark': 'red',
          'Norway': 'orange',
          'Finland': 'black',
          'Iceland': 'magenta'}
lines = {'df_deaths': 'solid',
         'Cases': 'dash',
         'ICU': 'dashdot'}

yaxis = {}

pops = {'Sweden': 10.036379,
        'Denmark': 5.771876,
        'Norway': 5.378857,
        'Finland': 5.532156,
        'Iceland': 0.339031}

fillcolors = {'Denmark': 'rgba(255, 0, 0, 0.05)',
              'Sweden': 'rgba(0,0,255,0.05)', }
# ("solid", "dot", "dash", "longdash", "dashdot", or "longdashdot")


def get_column_names(item):
    return plots[item]


def get_column_to_show(children):
    cols = []
    for child in children:
        if child['props']['active']:
            col = get_column_names(child['props']['id'])
            if "million" not in col:
                if 'poli' not in col:
                    cols.append(col)

    return cols


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
               ])
def update_total_deaths(countries, which_plots, start_date, end_date, scale, mobility, per_mn, check, check1, check2, political):
    if not countries or not start_date or not end_date:
        return html.Div()
    if not which_plots:
        return html.Div()
    columns = get_column_to_show(which_plots)
    if not columns:
        return html.Div()
    scale = next((s for s in scale), None)
    country_dicts = load_data()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    data = {}
    for country in countries:
        country_data = pd.DataFrame()
        for col in columns:

            if "ICU" in col and "Sweden" not in country:
                print("ok")
                continue
            elif "mobility" in col:
                try:
                    country_data[col] = country_dicts[country][col]
                except Exception as e:
                    continue
            else:
                if per_mn:
                    country_data[col] = country_dicts[country][col] / \
                        pops[country]
                else:
                    country_data[col] = country_dicts[country][col]
        data[country] = country_data[(country_data.index >= start_date)
                                     & (country_data.index <= end_date)]
        # for col in columns:
        #     if '1' in col:
        #         country_data = country_dicts[country][columns[:-2]]
        #         country_data = country_data[country_data > 0]
        #         country_data.index = range(len(country_data))
        #         # data[country] = country_dicts[country][]
        #     else:
    if mobility:

        fig = plot_graph_with_mobility(data, political, per_mn)
    else:

        fig = plot_graph(data, political, per_mn, scale)
    fig.update_layout(height=600)
    return dcc.Graph(id="Plot", figure=fig)


# @app.callback(Output('which_plot', 'children'),
#               [Input(f"{item}", 'n_clicks') for item in dfs])
# def button_pressed(db, dbmn, db1, dbmn1):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         button_id = 'df_deaths'
#     elif not db and not dbmn and not db1 and not dbmn1:
#         button_id = 'df_deaths'
#     else:
#         button_id = ctx.triggered[0]['prop_id'].split('.')[0]

#     return json.dumps({'button_pressed': button_id})


@app.callback([Output('picked-dates', 'min_date_allowed'),
               Output('picked-dates', 'max_date_allowed'),
               Output('picked-dates', 'start_date'),
               Output('picked-dates', 'end_date')],
              [Input('data', 'children')])
def get_date_picker(json_obj):
    if not json:
        return None
    with open('dates.pkl', 'rb') as f:
        dates = pickle.load(f)['death_dates']
    start_date = dates[0]
    end_date = dates[-1]
    return start_date, end_date + timedelta(days=1), start_date, end_date

# @app.callback(Output('visible_dates', 'style'),
#               [Input('which_plot', 'children')])
# def visible_date_picker(plot_json):
#     plot = json.loads(plot_json)['button_pressed']
#     if plot not in ['df_deaths', 'df_deaths_per_mn']:
#         return {'display': 'none'}
#     else:
#         return {'display': 'inline-block'}


@app.callback(Output('Map', 'children'),
              [Input('date-slider', 'value'),
               Input('map_total_cases', 'active'),
               Input('map_iva_patients', 'active'),
               Input('map_death', 'active'),
               Input('mobility_map', 'active')])
def plot_map(date_index, total, iva, death, mobility):
    date = get_date_from_index(date_index)
    column = "Deaths"
    if total:
        column = "Tested_Confirmed"
    if death:
        column = "Deaths"
    if iva:
        column = "ICU_Patients"
    if mobility:
        column = "Mobility"
    print(column)
    from urllib.request import urlopen
    import json
    import plotly
    # Example data
    with open('data/features.geojson') as response:
        counties = json.load(response)
    import plotly.express as px
    df = pd.read_csv('data/map_data.csv')
    print(column)
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
    map_graph = dcc.Graph(id="Map", figure=fig)
    return html.Div([map_graph])

@app.callback(Output('selected-date-map', 'children'),
              [Input('date-slider', 'value')])
def get_selected_map_date(date_index):
    date = get_date_from_index(date_index)
    date_string = date.strftime("%d %b")
    return html.Label("Date "+date_string)

# @app.callback([Output(f"{item}", 'active') for item in dfs],
#               [Input(f"{item}", 'n_clicks') for item in dfs])
# def update_active_button(d, dpm, d1, dpm1):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         button_id = 'df_deaths'
#     else:
#         button_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     if not d and not dpm and not d1 and not dpm1:
#         button_id = 'df_deaths'
#     updating = [True if item == button_id else False for item in dfs]
#     return updating


@app.callback([Output(f"{item}", 'active') for item in active_map],
              [Input(f"{item}", 'n_clicks')for item in active_map],
              [State(f"{item}", 'active') for item in active_map]
              )
def update_active_button(death, cases, iva, mobility, death_state, cases_state, iva_state, mobility_state):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'mobility_map'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if not death and not cases and not iva:
        button_id = 'mobility_map'
        updating = [False, False, False, True]
    else:
        states = [death_state, cases_state, iva_state, mobility_state]
        updating = [False if button_id not in active else True for state,
                    active in zip(states, active_map)]

    return updating


@app.callback(Output("mobility_index", 'active'),
              [Input("mobility_index", 'n_clicks')],
              [State("mobility_index", 'active')])
def change_mobility_visibility(mobility, mobility_active):
    if not mobility:
        return mobility_active

    return not mobility_active


@app.callback(Output("ICU", 'active'),
              [Input("ICU", 'n_clicks')],
              [State("ICU", 'active')])
def change_icu_visibility(icu, icu_active):
    if not icu:
        return icu_active
    return not icu_active


@app.callback(Output("death", 'active'),
              [Input("death", 'n_clicks')],
              [State("death", 'active')])
def change_icu_visibility(death, death_active):
    if not death:
        return death_active
    return not death_active


@app.callback(Output("political", 'active'),
              [Input("political", 'n_clicks')],
              [State("political", 'active')])
def change_icu_visibility(political, political_active):
    if not political:
        return political_active
    return not political_active


@app.callback(Output("per_million", 'active'),
              [Input("per_million", 'n_clicks')],
              [State("per_million", 'active')])
def change_icu_visibility(pm, pm_active):
    if not pm:
        return pm_active
    return not pm_active


@app.callback(Output("confirmed", 'active'),
              [Input("confirmed", 'n_clicks')],
              [State("confirmed", 'active')])
def change_icu_visibility(confirmed, confirmed_active):
    if not confirmed:
        return confirmed_active
    return not confirmed_active


def plot_graph_with_mobility(data, politics, per_mn, scale="linear"):
    titley = ''
    if per_mn:
        titley = "Number of peopler per Million"
    else:
        titley = "Number of People"
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    max_val = 0
    for country, df in data.items():
        color = colors[country]
        for col in df.columns:
            if 'mobility' not in col:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[col], name=country+' '+legends[col], line={'dash': lines[col], 'color': color},), secondary_y=True)
            else:
                if max_val < df[col].max():
                    max_val = df[col].max()
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[col], name="Mobility " + country, fill='tozeroy', fillcolor=fillcolors[country], line={'color': color}), secondary_y=False
                )

    fig.update_layout(template="plotly_white", title_text="Covid 19 Analysis",
                      # xaxis=dict(tickmode='linear', fixedrange=True), xaxis_range=[data.index[0], end_date],
                      xaxis_title="Dates",
                      hovermode='x',
                      xaxis_rangeslider_visible=False)  # annotations=[dict(x=1, y=0, text="Updated {}".format(str(date)[:10] + ' 03:00 CET'),
    #                  showarrow=False, xref='paper', yref='paper',
    #                 xanchor='right', yanchor='bottom', xshift=0, yshift=0, font=dict(color="red", size=8.5))])
    fig.update_yaxes(title_text="Mobility %",
                     secondary_y=False)

    fig.update_yaxes(title_text=titley, secondary_y=True)
    if politics:
        fig = add_political_decision(fig, max_val)

    return fig


def plot_graph(data, politics, per_mn, scale='linear', end_date=None):
    titley = ''
    if per_mn:
        titley = "Number of peopler per Million"
    else:
        titley = "Number of People"
    fig = go.Figure()
    # if not end_date:
    #     if isinstance(end_date, int):
    #         end_date = end_date + 1
    #     else:
    #         end_date = end_date + timedelta(days=1)
    max_val = 0
    for country, df in data.items():
        color = colors[country]
        for col in df.columns:
            if max_val < df[col].max():
                max_val = df[col].max()

            fig.add_trace(go.Scatter(
                x=df.index, y=df[col], name=country+' '+legends[col], line={'dash': lines[col], 'color': color}))
    fig.update_layout(template="plotly_white", title_text="Covid 19 Analysis",
                      # xaxis=dict(tickmode='linear', fixedrange=True), xaxis_range=[data.index[0], end_date],
                      xaxis_title="Dates",
                      yaxis_title=titley, yaxis=dict(fixedrange=True),
                      hovermode='x',
                      xaxis_rangeslider_visible=False)  # annotations=[dict(x=1, y=0, text="Updated {}".format(str(date)[:10] + ' 03:00 CET'),
    #                  showarrow=False, xref='paper', yref='paper',
    #                 xanchor='right', yanchor='bottom', xshift=0, yshift=0, font=dict(color="red", size=8.5))])
    if scale == 'on':
        fig.update_layout(yaxis_type='log', yaxis_exponentformat="power")
    if politics:
        fig = add_political_decision(fig, max_val)

    return fig


def add_political_decision(fig, max_val, politics=False):
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
        #hovertemplate="y: %{max_val}",
        # hovertext='text',
        hoverlabel=dict(bgcolor='rgba(7, 164, 181, 0.5)'),
        marker=dict(color=px.colors.sequential.RdBu[-2]), name='Swedish Political Decisions'))

    fig.update_layout(
        # Line Vertical
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


def get_date_from_index(date_index):
    with open('dates.pkl', 'rb') as f:
        dates = pickle.load(f)['confirmed_dates']
    date = dates[date_index]
    return date


if __name__ == "__main__":
    app.run_server(debug=True)
    pass


"""@app.callback([Output("linear-button", 'active'),
               Output("log-button", 'active')],
              [Input("linear-button", 'n_clicks'),
               Input("log-button", 'n_clicks')])
def update_scale_button(linear, log):
    buttons = ['linear-button', 'log-button']
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'linear-button'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if not linear and not log:
        button_id = 'linear-button'
    updating = [True if item == button_id else False for item in buttons]
    return updating


@app.callback(Output('which_scale', 'children'),
              [Input("linear-button", 'n_clicks'),
               Input("log-button", 'n_clicks')])
def update_selected_scale(linear, log):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'linear-button'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if not linear and not log:
        button_id = 'linear-button'
    return json.dumps({'button': button_id.split('-')[0]})
"""
