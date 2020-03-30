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


import layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
tmp = dbc.themes.BOOTSTRAP
with open("check.txt", 'w') as f:
    f.writelines(tmp)

server = app.server

app.layout = layout.generate_layout()

dfs = ['df_deaths', 'df_deaths_per_mn', 'df_deaths_1', 'df_deaths_per_mn_1']
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


@app.callback(Output('deaths_plot', 'children'),
              [Input('country_selection', 'value'),
               Input('which_plot', 'children'),
               Input('picked-dates', 'start_date'),
               Input('picked-dates', 'end_date'),
               Input('log-scale', 'value')],
              [State('data', 'children')])
def update_total_deaths(countries, which_plot_json, start_date, end_date, scale, json_obj):
    if not json_obj or not countries or not start_date or not end_date:
        return html.Div()
    which_plot = json.loads(which_plot_json)['button_pressed']
    obj = json.loads(json_obj)
    scale = next((s for s in scale), None)
    data = pd.read_json(obj[which_plot])
    date = datetime.fromtimestamp(obj['date'])
    if which_plot in ['df_deaths', 'df_deaths_per_mn']:
        data = data[(data.index >= start_date)
                    & (data.index <= end_date)]
    title = titles[which_plot]
    x_title = x_axis_labels[which_plot]
    y_title = y_axis_labels[which_plot]
    data = data[countries]

    fig = plot_graph(data, title, x_title, y_title,
                     date, scale, template="plotly_white")
    fig.update_layout(height=600)
    return dcc.Graph(id="Plot", figure=fig)


@app.callback(Output('which_plot', 'children'),
              [Input(f"{item}", 'n_clicks') for item in dfs])
def button_pressed(db, dbmn, db1, dbmn1):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'df_deaths'
    elif not db and not dbmn and not db1 and not dbmn1:
        button_id = 'df_deaths'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    return json.dumps({'button_pressed': button_id})


@app.callback([Output('picked-dates', 'min_date_allowed'),
               Output('picked-dates', 'max_date_allowed'),
               Output('picked-dates', 'start_date'),
               Output('picked-dates', 'end_date')],
              [Input('data', 'children')])
def get_date_picker(json_obj):
    if not json:
        return None

    df = pd.read_json(json.loads(json_obj)['df_deaths'])
    start_date = df.index[0]
    end_date = df.index[-1]
    return start_date, end_date + timedelta(days=1), start_date, end_date

@app.callback(Output('visible_dates', 'style'),
              [Input('which_plot', 'children')])
def visible_date_picker(plot_json):
    plot = json.loads(plot_json)['button_pressed']
    if plot not in ['df_deaths', 'df_deaths_per_mn']:
        return {'display': 'none'}
    else:
        return {'display': 'inline-block'}


@app.callback([Output(f"{item}", 'active') for item in dfs],
              [Input(f"{item}", 'n_clicks') for item in dfs])
def update_active_button(d, dpm, d1, dpm1):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'df_deaths'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if not d and not dpm and not d1 and not dpm1:
        button_id = 'df_deaths'
    updating = [True if item == button_id else False for item in dfs]
    return updating


def plot_graph(data, title, x_title, y_title, date, scale='linear', template='seaborn', end_date=None):
    fig = go.Figure()
    if not end_date:
        end_date = data.index[-1]
        if isinstance(end_date, np.integer):
            end_date = end_date + 1
        else:
            end_date = end_date + timedelta(days=1)
    for col in data:
        fig.add_trace(go.Scatter(x=data.index, y=data[col], name=col))
    fig.update_layout(template=template, title_text=title,
                      xaxis_title=x_title, xaxis=dict(tickmode='linear', fixedrange=True), xaxis_range=[data.index[0], end_date],
                      yaxis_title=y_title, yaxis=dict(fixedrange=True),
                      hovermode='x',
                      xaxis_rangeslider_visible=False, annotations=[dict(x=1, y=0, text="Updated {}".format(str(date)[:10] + ' 03:00 CET'),
                                                                         showarrow=False, xref='paper', yref='paper',
                                                                         xanchor='right', yanchor='bottom', xshift=0, yshift=0, font=dict(color="red", size=8.5))])
    if scale == 'on':
        fig.update_layout(yaxis_type='log', yaxis_exponentformat="power")
    return fig


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
