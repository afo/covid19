import dash
import dash_core_components as dcc
import dash_html_components as html

from extract_data import get_data


def generate_layout():
    layout = html.Div(className='container', children=[
        html.Div(className="app-header",
                 children=[html.Div("COVID19 Nordic Analysis", className="app-header--title")]),
        dcc.Tabs(children=[
            dcc.Tab(label="Total Deaths since March 10", id="Tab 1", children=[
                html.Div("Subheader", className="app-subheader"),
                checkboxes("1"),
                dcc.Graph(id="deaths_plot")
            ]),
            dcc.Tab(label="Map Preliminary", id="Tab 2", children=[
            ])
        ]),
        html.Div(id="data", style={'display': 'none'}, children=get_data())
    ])
    return layout


def checkboxes(tab_name):
    plots = plot_selection(tab_name)
    countries = country_selection(tab_name)
    plot_div = html.Div(children=[plots])
    country_div = html.Div(children=[countries], style={
        'display': 'inline-block'})
    return html.Div(children=[plot_div, country_div])


def plot_selection(tab_name):
    options = [{
        'label': 'Total Deaths',
        'value': 'df_deaths',
    },
        {
        'label': 'Total Deaths per Mn',
        'value': 'df_deaths_per_mn',
    },
        {
        'label': 'Deaths since first',
        'value': 'df_deaths_1',
    },
        {
        'label': 'Deaths since first death per mn',
        'value': 'df_deaths_per_mn_1',
    }]
    radio = dcc.RadioItems(id=f"which_plot{tab_name}", options=options, labelStyle={
        'display': 'inline-block'}, value='df_deaths')
    return radio


def country_selection(tab_name):
    options = [{
        'label': '🇸🇪 Sweden',
        'value': 'Sweden'
    },
        {
        'label': '🇫🇮 Finland',
        'value': 'Finland'
    },
        {
        'label': '🇳🇴 Norway',
        'value': 'Norway'
    },
        {
        'label': '🇩🇰 Denmark',
        'value': 'Denmark'
    },
        {
        'label': '🇮🇸 Iceland',
        'value': 'Iceland'
    }]

    value = ["Sweden", "Norway", "Finland", "Denmark", "Iceland"]
    checklist = dcc.Dropdown(id=f"country_selection{tab_name}", multi=True,
                             options=options, value=value)
    return checklist
