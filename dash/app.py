import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime, timedelta
import json
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
         'per_million': 'million'}
countries = ['Sweden', 'Finland', 'Denmark', 'Norway', 'Iceland']
active_map = ["map_death", 'map_total_cases', 'map_iva_patients']
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

colors = {'Sweden': 'blue',
          'Denmark': 'red',
          'Norway': 'orange',
          'Finland': 'black',
          'Iceland': 'magenta'}
lines = {'df_deaths': 'solid',
         'Cases': 'dash',
         'ICU': 'dashdot'}

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
               ])
def update_total_deaths(countries, which_plots, start_date, end_date, scale, mobility, per_mn, check, check1, check2):
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
    print(per_mn)
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

        fig = plot_graph_with_mobility(data)
    else:

        fig = plot_graph(data, scale)
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
              [Input('date-slider', 'value')])
def plot_map(date_index):
    date = get_date_from_index(date_index)

    fig = go.Figure(data=go.Choropleth(
        colorscale='greens',
    ))

    fig.update_layout(
        title_text='Regional Data',
        geo_scope='europe',  # limite map scope to USA
    )
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
def update_active_button(death, cases, iva, death_state, cases_state, iva_state):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'map_death'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if not death and not cases and not iva:
        button_id = 'map_death'
        updating = [True, False, False]
    else:
        states = [death_state, cases_state, iva_state]
        updating = [state if button_id not in active else not state for state,
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
# @app.callback([Output(f"{item}", 'active') for item in countries],
#               [Input(f"{item}", 'n_clicks')for item in countries],
#               [State(f"{item}", 'active') for item in countries]
#               )
# def update_active_button(sweden, finland, denmark, norway, iceland,
#                          sweden_active, finland_active, denmark_active, norway_active, iceland_active):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         button_id = 'Sweden'
#         [True, True, True, True, True]
#     else:
#         button_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     if not sweden and not finland and not denmark and not norway and not iceland:
#         button_id = ''
#         updating = [True, True, True, True, True]
#     else:
#         states = [sweden_active, finland_active,
#                   denmark_active, norway_active, iceland_active]
#         updating = [state if button_id not in active else not state for state,
#                     active in zip(states, countries)]
#     return updating


def plot_graph_with_mobility(data, scale='linear'):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for country, df in data.items():
        color = colors[country]
        for col in df.columns:
            print(col)
            if 'mobility' not in col:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[col], name=country+col, line={'dash': lines[col], 'color': color},), secondary_y=True)
            else:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[col], name="mobility " + country, fill='tozeroy', fillcolor=fillcolors[country], line={'color': color}), secondary_y=False
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

    fig.update_yaxes(title_text="Number of People", secondary_y=True)

    return fig


def plot_graph(data, scale='linear', end_date=None):
    fig = go.Figure()
    # if not end_date:
    #     if isinstance(end_date, int):
    #         end_date = end_date + 1
    #     else:
    #         end_date = end_date + timedelta(days=1)
    for country, df in data.items():
        color = colors[country]
        for col in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df[col], name=country+col, line={'dash': lines[col], 'color': color}))
    fig.update_layout(template="plotly_white", title_text="Covid 19 Analysis",
                      # xaxis=dict(tickmode='linear', fixedrange=True), xaxis_range=[data.index[0], end_date],
                      xaxis_title="Dates",
                      yaxis_title="Number of people", yaxis=dict(fixedrange=True),
                      hovermode='x',
                      xaxis_rangeslider_visible=False)  # annotations=[dict(x=1, y=0, text="Updated {}".format(str(date)[:10] + ' 03:00 CET'),
    #                  showarrow=False, xref='paper', yref='paper',
    #                 xanchor='right', yanchor='bottom', xshift=0, yshift=0, font=dict(color="red", size=8.5))])
    if scale == 'on':
        fig.update_layout(yaxis_type='log', yaxis_exponentformat="power")
    return fig


# def plot_graph(data, x_title, date, scale='linear', end_date=None):
#     fig = go.Figure()
#     if not end_date:
#         end_date = data.index[-1]
#         if isinstance(end_date, int):
#             end_date = end_date + 1
#         else:
#             end_date = end_date + timedelta(days=1)
#     for col in data:
#         fig.add_trace(go.Scatter(x=data.index, y=data[col], name=col))
#     fig.update_layout(template="plotly_white", title_text="Covid 19 Analysis",
#                       xaxis_title='Dates', xaxis=dict(tickmode='linear', fixedrange=True), xaxis_range=[data.index[0], end_date],
#                       yaxis_title="Selected inputs", yaxis=dict(fixedrange=True),
#                       hovermode='x',
#                       xaxis_rangeslider_visible=False, annotations=[dict(x=1, y=0, text="Updated {}".format(str(date)[:10] + ' 03:00 CET'),
#                                                                          showarrow=False, xref='paper', yref='paper',
#                                                                          xanchor='right', yanchor='bottom', xshift=0, yshift=0, font=dict(color="red", size=8.5))])
#     if scale == 'on':
#         fig.update_layout(yaxis_type='log', yaxis_exponentformat="power")
#     return fig


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
