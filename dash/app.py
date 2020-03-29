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
               Input('which_plot1', 'value')])
def update_total_deaths(json_obj, countries, which_plot):
    if not json_obj or not countries:
        return go.Figure()
    df_deaths = pd.read_json(json.loads(json_obj)[which_plot])
    title = titles[which_plot]
    fig = go.Figure()
    for col in countries:
        fig.add_trace(go.Scatter(x=df_deaths.index,
                                 y=df_deaths[col], name=col))

    fig.update_layout(template='plotly_white', title_text='COVID19 Total Nordic Deaths, daily data since first death',
                      xaxis_title=x_axis_labels[which_plot],
                      yaxis_title=y_axis_labels[which_plot],
                      hovermode='x',
                      height=600,
                      xaxis_rangeslider_visible=True,
                      annotations=[dict(x=1,
                                        y=-.47,
                                        text="Updated {}".format(
                                            str(df_deaths.tail().index[-1])[:10]),
                                        showarrow=False, xref='paper', yref='paper',
                                        xanchor='right', yanchor='auto', xshift=0, yshift=0,
                                        font=dict(color="red", size=12))])

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
    pass
