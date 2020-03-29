import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import json
from dash.dependencies import Input, Output

import layout

app = dash.Dash()

app.layout = layout.generate_layout()

<<<<<<< HEAD

@app.callback(Output('total_deaths', 'figure'),
              [Input('data', 'children'),
               Input('country_selection1', 'value')])
def update_total_deaths(json_obj, countries):
    if not json_obj or not countries:
        return go.Figure()
    df_deaths = pd.read_json(json.loads(json_obj)['deaths'])
=======
titles = {'df_deaths': 'COVID19 Total Nordic Deaths, starting March 10 2020',
          'df_deaths_per_mn': 'COVID19 Total Nordic Deaths per Mn inhabitants, starting March 10 2020',
          'df_deaths_1': 'COVID19 Total Nordic Deaths, daily data since first death',
          'df_deaths_per_mn_1': 'COVID19 Total Nordic Deaths per Mn inhabitants, daily data since first death'}


@app.callback(Output('deaths_plot', 'figure'),
              [Input('data', 'children'),
               Input('country_selection1', 'value'),
               Input('which_plot1', 'value')])
def update_total_deaths(json_obj, countries, which_plot):
    if not json_obj or not countries:
        return go.Figure()
    df_deaths = pd.read_json(json.loads(json_obj)[which_plot])
    title = titles[which_plot]
>>>>>>> Added dash functionality. Please take a look bro
    fig = go.Figure()
    for col in countries:
        fig.add_trace(go.Scatter(x=df_deaths.index,
                                 y=df_deaths[col], name=col))
<<<<<<< HEAD
    fig.update_layout(title_text='COVID19 Total Nordic Deaths, starting March 10 2020', hovermode='x',
                      xaxis_rangeslider_visible=True)

    return fig


@app.callback(Output('Deaths/mn', 'figure'),
              [Input('data', 'children'),
               Input('country_selection2', 'value')])
def update_total_deaths(json_obj, countries):
    if not json_obj or not countries:
        return go.Figure()
    df_deaths_per_mn = pd.read_json(json.loads(json_obj)['deaths_per_mn'])

    fig = go.Figure()
    for col in countries:
        fig.add_trace(go.Scatter(x=df_deaths_per_mn.index,
                                 y=df_deaths_per_mn[col], name=col))

    fig.update_layout(title_text='COVID19 Total Nordic Deaths per Mn inhabitants, starting March 10 2020', hovermode='x',
=======
    fig.update_layout(title_text=title, hovermode='x',
>>>>>>> Added dash functionality. Please take a look bro
                      xaxis_rangeslider_visible=True)

    return fig


<<<<<<< HEAD
@app.callback(Output('daily_deaths', 'figure'),
              [Input('data', 'children'),
               Input('country_selection3', 'value')])
def update_total_deaths(json_obj, countries):
    if not json_obj or not countries:
        return go.Figure()
    df_deaths_1 = pd.read_json(json.loads(json_obj)['deaths_1'])

    fig = go.Figure()
    for col in countries:
        fig.add_trace(go.Scatter(x=df_deaths_1.index,
                                 y=df_deaths_1[col], name=col))

    fig.update_layout(template='plotly_white', title_text='COVID19 Total Nordic Deaths, daily data since first death', hovermode='x',
                      xaxis_rangeslider_visible=True)
    return fig


@app.callback(Output('daily_deaths/mn', 'figure'),
              [Input('data', 'children'),
               Input('country_selection4', 'value')])
def update_total_deaths(json_obj, countries):
    if not json_obj or not countries:
        return go.Figure()
    df_deaths_per_mn_1 = pd.read_json(json.loads(json_obj)['deaths_per_mn_1'])

    fig = go.Figure()
    for col in countries:
        fig.add_trace(go.Scatter(x=df_deaths_per_mn_1.index,
                                 y=df_deaths_per_mn_1[col], name=col))

    fig.update_layout(template='plotly_white', title_text='COVID19 Total Nordic Deaths per Mn inhabitants, daily data since first death', hovermode='x',
                      xaxis_rangeslider_visible=True)
    return fig


=======
>>>>>>> Added dash functionality. Please take a look bro
if __name__ == "__main__":
    app.run_server(debug=True)
    pass
