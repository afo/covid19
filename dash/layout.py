import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from extract_data import get_data


def generate_layout():
    layout = html.Div(className='container', children=[
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
        generate_scale_buttons(),
        # dcc.Tab(label="Map Preliminary", id="Tab 2", children=[
        # ])
        html.Div(id="which_scale", style={'display': 'none'}),
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
    deaths = dbc.Button('1. Deaths', id="df_deaths",
                        color="primary")
    deaths_mn = dbc.Button(
        '2. Deaths per Mn', id="df_deaths_per_mn", color="primary",)
    deaths_1 = dbc.Button('3. Deaths since first',
                          id="df_deaths_1", color="primary", )
    deaths_mn_1 = dbc.Button('4. Deaths per Mn since first', id="df_deaths_per_mn_1",
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


def generate_scale_buttons():
    linear_button = dbc.Button("Linear", id="linear-button", color="Primary", size="sm")
    log_button = dbc.Button("Log", id="log-button", color="primary", size="sm")
    return html.Div([linear_button, log_button])
