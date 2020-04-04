import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pickle

from extract_data import get_data


def generate_layout():
    layout = html.Div(className='container', children=[
        dcc.Tabs([
            dcc.Tab(label="Death Analysis", children=[html.Div([
                html.Div("Select plot", className="app-subheader"),
                generate_buttons(),
                html.Hr(),
                html.Label("Countries", style={'font-weight': 'bold'}),
                html.Br(),
                country_selection(),
                html.Br(),
                html.Div([html.Div(id="visible_dates", children=[html.Label("Select date interval", style={'font-weight': 'bold'}),
                                                                 html.Br(),
                                                                 dcc.DatePickerRange(
                    id='picked-dates')
                ], className="five columns", style={'display': 'inline-block'}),
                    html.Div([html.Br(), html.Br(className="br-2"), dbc.Checklist(
                        options=[{'label': 'Log Scale', 'value': 'on'}], value=[], id="log-scale", switch=True)], className="three columns")
                ], className="twelve columns"),
                html.Div([html.Div(id="deaths_plot")],
                         className="twelve columns"),
            ])]),
            dcc.Tab(label="Regional map", children=[
                html.Br(),
                html.Br(),
                html.Div([
                    html.Div(html.Label("Show"), className="three columns", style={
                             'text-align': 'center'}),
                    html.Div(dbc.ButtonGroup(
                        generate_map_buttons()), className="six columns")
                ], className="twelve columns"),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Div([
                    html.Div([html.Label("Move Forward in time")],
                             className="three columns", style={
                             'text-align': 'center'}),
                    html.Div(generate_date_slider(), className="six columns"),
                    html.Div(id="selected-date-map", style={
                        'text-align': 'center'})], className='twelve columns'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Div([
                    html.Div(id="Map")
                ])]),

            html.Div(id="data", style={
                     'display': 'none'}, children=get_data()),
            html.Div(id="which_plot", style={'display': 'none'})
        ])])
    return layout


def checkboxes(tab_name):
    countries = country_selection(tab_name)
    country_div = html.Div(children=[countries], style={
        'display': 'inline-block'})
    buttons = generate_buttons()
    return html.Div(children=[country_div, buttons])


def generate_buttons():
    deaths = dbc.Button('Deaths', id="df_deaths")
    deaths_mn = dbc.Button(
        'Deaths per Mn', id="df_deaths_per_mn")
    deaths_1 = dbc.Button('Deaths since first',
                          id="df_deaths_1")
    deaths_mn_1 = dbc.Button(
        'Deaths per Mn since first', id="df_deaths_per_mn_1")
    return html.Div(children=[deaths, deaths_mn, deaths_1, deaths_mn_1])


def generate_map_buttons():
    deaths = dbc.Button("Total deaths", id="map_death")
    total_cases = dbc.Button("Total Cases", id='map_total_cases')
    iva_cases = dbc.Button("Total IVA-patients", id='map_iva_patients')
    return [deaths, total_cases, iva_cases]


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
    linear_button = dbc.Button(
        "Linear", id="linear-button", color="Primary", size="sm")
    log_button = dbc.Button("Log", id="log-button", color="primary", size="sm")
    return html.Div([linear_button, log_button])


def generate_date_slider():
    with open('dates.pkl', 'rb') as f:
        dates = pickle.load(f)['confirmed_dates']
    min = 0
    max = len(dates)
    marks_alls = {i: date.strftime("%B") for i, date in enumerate(dates)}
    marks_used = {}
    months = [marks_alls[0]]
    for k, v in marks_alls.items():
        if v not in months:
            marks_used[k] = v
            months.append(v)
    slider = dcc.Slider(id="date-slider", min=min, max=max,
                        marks=marks_used, value=50)
    return slider
