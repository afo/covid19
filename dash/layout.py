import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from extract_data import get_data


def generate_layout():
    layout = html.Div(className='container', children=[
        html.Div(className="app-header",
                 children=[html.Div("COVID19 in the Nordics", className="app-header--title")]),
        html.Div("Select plot", className="app-subheader"),
        generate_buttons(),
        html.Label("Countries", style={'font-weight': 'bold'}),
        country_selection(),
        html.Br(),
        html.Div(id="visible_dates", children=[html.Label("Select date interval", style={'font-weight': 'bold'}),
                                               dcc.DatePickerRange(
                                                   id='picked-dates')
                                               ], style={'margin': 'auto'}),
        html.Div(id="deaths_plot"),
        # dcc.Tab(label="Map Preliminary", id="Tab 2", children=[
        # ])
        html.Div(id="data", style={'display': 'none'}, children=get_data()),
        html.Div(id="which_plot", style={'display': 'none'})
    ])
    return layout


def checkboxes(tab_name):
    countries = country_selection(tab_name)
    country_div = html.Div(children=[countries], style={
        'display': 'inline-block'})
    buttons = generate_buttons()
    return html.Div(children=[country_div, buttons])


def generate_buttons():
    deaths = dbc.Button('Deaths', id="df_deaths",
                        color="primary")
    deaths_mn = dbc.Button(
        'Deaths per Mn', id="df_deaths_per_mn", color="primary",)
    deaths_1 = dbc.Button('Deaths since first',
                          id="df_deaths_1", color="primary", )
    deaths_mn_1 = dbc.Button('Deaths per Mn since first', id="df_deaths_per_mn_1",
                             color="primary", )
    return html.Div(children=[deaths, deaths_mn, deaths_1, deaths_mn_1])


def country_selection():
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
    checklist = dcc.Dropdown(id=f"country_selection", multi=True,
                             options=options, value=value)
    return html.Div([checklist], style={'display': 'inline-block'})
