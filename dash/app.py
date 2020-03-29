import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
from dash.dependencies import Input, Output

import layout

app = dash.Dash()

app.layout = layout.generate_layout()


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
              [Input('data', 'children'),
               Input('country_selection1', 'value'),
               Input('which_plot1', 'value'),
               Input('picked-dates', 'start_date'),
               Input('picked-dates', 'end_date')])
def update_total_deaths(json_obj, countries, which_plot, start_date, end_date):
    if not json_obj or not countries or not start_date or not end_date:
        return go.Figure()
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
              [Input('which_plot1', 'value')])
def visible_date_picker(plot):
    if plot not in ['df_deaths', 'df_deaths_per_mn']:
        return {'display': 'none'}
    else:
        return {'display': 'inline-block'}


def plot_graph(data, title, x_title, y_title, date, template='seaborn', end_date=None):
    fig = go.Figure()
    if not end_date:
        end_date = data.index[-1]
    for col in data:
        fig.add_trace(go.Scatter(x=data.index, y=data[col], name=col))
    print(end_date)
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
