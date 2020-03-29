import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
from dash.dependencies import Input, Output, State

import layout

app = dash.Dash()

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


@app.callback(Output('deaths_plot', 'figure'),
              [Input('country_selection1', 'value'),
               Input('which_plot', 'children'),
               Input('picked-dates', 'start_date'),
               Input('picked-dates', 'end_date')],
              [State('data', 'children')])
def update_total_deaths(countries, which_plot_json, start_date, end_date, json_obj):
    if not json_obj or not countries or not start_date or not end_date:
        return go.Figure()
    which_plot = json.loads(which_plot_json)['button_pressed']
    obj = json.loads(json_obj)
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
                     date, template="plotly_white")
    fig.update_layout(height=600)
    return fig


@app.callback(Output('which_plot', 'children'),
              [Input(f"{item}", 'n_clicks') for item in dfs])
def button_pressed(db, dbmn, db1, dbmn1):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'df_deaths'
    elif not db or not dbm or not db1 or not dbmn1:
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
    return start_date, end_date, start_date, end_date

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


def plot_graph(data, title, x_title, y_title, date, template='seaborn', end_date=None):
    fig = go.Figure()
    if not end_date:
        end_date = data.index[-1]
    for col in data:
        fig.add_trace(go.Scatter(x=data.index, y=data[col], name=col))
    fig.update_layout(template=template, title_text=title,
                      xaxis_title=x_title, xaxis=dict(tickmode='linear'), xaxis_range=[data.index[0], end_date],
                      yaxis_title=y_title,
                      hovermode='x',
                      xaxis_rangeslider_visible=True, annotations=[dict(x=1, y=0, text="Updated {}".format(date),
                                                                        showarrow=False, xref='paper', yref='paper',
                                                                        xanchor='right', yanchor='bottom', xshift=0, yshift=0, font=dict(color="red", size=8.5))])
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
    pass
