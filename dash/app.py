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
    fig.update_layout(title_text=title, hovermode='x',
                      xaxis_rangeslider_visible=True)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
    pass
