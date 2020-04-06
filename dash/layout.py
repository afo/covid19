import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pickle

from extract_data import get_data


def generate_layout():
    """Generates the defualt layout for the dashboard

    TODO(@andreasfo@gmail.com)
    Fix to a much more readable format, too much ugliness inside

    Returns:
        dash html.Div -- layout of the dashboard
    """
    layout = html.Div(className='container', children=[
        dcc.Tabs(
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[dcc.Tab(label="Nordic Analysis", children=[html.Div([
                html.Div("Select Inputs", className="app-subheader"),
                html.Hr(),
                # html.Div([
                html.Label("Countries", style={
                    'font-weight': 'bold', 'font-size': '18px'}),
                #     country_buttons(),
                # ]),
                html.Br(),
                country_selection(),
                html.Br(),
                html.Label("Select Features", style={
                           'font-weight': 'bold', 'font-size': '18px'}),
                html.Div(children=generate_option_buttons(),
                         id="testing",
                         style={'display': 'inline-block'}, className="twelve columns"),
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
            ])], className='custom-tab',
                selected_className='custom-tab--selected'),
                dcc.Tab(label="Swedish Regional Map", children=[
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
                        html.Div(generate_date_slider(),
                                 className="six columns"),
                        html.Div(id="selected-date-map", style={
                            'text-align': 'center'})], className='twelve columns'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Div(id="Map")
                    ])], className='custom-tab',
                selected_className='custom-tab--selected'),

                html.Div(id="data", style={
                    'display': 'none'}, children=get_data()),
                html.Div(id="which_plot", style={'display': 'none'})
            ])])
    return layout


def generate_option_buttons():
    """Generates button used for options

    Buttons used to select which  feature(s) is going to be shown in
    the main dashboard plot.

    Current buttons:
        -death
            Show total amount of deaths
        -mobility
            Show mobility index
        -ICU
            Show intensive care patients
        -Confirmed
            Show confirmed cases
        -Pop
            Show feature per million inhabitants instead
        -Political
            Show political decisions instead

    Returns:
        List  of dbc.Buttons -- 
    """
    dropdown_mobility = dbc.Button(
        "Mobility", active=False,
        id="mobility_index"
    )
    dropdown_icu = dbc.Button("ICU Cases", active=False, id="ICU")
    dropdown_confirmed = dbc.Button(
        "Confirmed Cases", active=False, id="confirmed")
    death = dbc.Button("Deaths", active=True, id="death")
    pop_button = dbc.Button("Per Million", active=False, id="per_million")
    political = dbc.Button("Political Decisions", active=False, id="political")
    return [death, dropdown_mobility, dropdown_icu, dropdown_confirmed, pop_button, political]


def country_buttons():
    """Generates the country buttons for the layout


    TODO(@andreasfo@gmail.com)
        Fix to use this one instead of the dropdown menu
    Returns:
        dbcButtonGroup -- A  button group of all countries
    """
    countries = [{'label': '🇸🇪 Sweden',
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
    button_style = {
        'padding': '.25rem .5rem',
        'font-size': '10px',
        'line-height': '1',
        'border-radius': '10px',
        'height': '25px',
        'align-items': 'center',
        'justify-content': 'center',
    }
    buttons = []
    for country in countries:
        buttons.append(dbc.Button(
            country['label'], id=country['value'], style=button_style))

    return dbc.ButtonGroup(buttons, id="country_buttons")


def generate_map_buttons():
    """Generates the buttons used to switch the map view

    TODO(@andreasfo@gmail.com)
    Returns:
        List of dbc.Buttons -- Buttons to select map view
    """
    deaths = dbc.Button("Total deaths", id="map_death")
    total_cases = dbc.Button("Total Cases", id='map_total_cases')
    iva_cases = dbc.Button("Total IVA-patients", id='map_iva_patients')
    mobility = dbc.Button("Mobility Index", id="mobility_map")
    return [deaths, total_cases, iva_cases, mobility]


def country_selection():
    """Generates the country selection dropdown 

    Returns:
        Dash html.Div -- Div of the country selection menu
    """
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
    """Create the log scale  on-off button

    Returns:
        Dash  html.Div -- scalebutton
    """
    linear_button = dbc.Button(
        "Linear", id="linear-button", color="Primary", size="sm")
    log_button = dbc.Button("Log", id="log-button",
                            color="primary", size="sm")
    return html.Div([linear_button, log_button])


def generate_date_slider():
    """Generates the Date slider for map

    Returns:
        Dash core compnent  Slider -- Date slider for map
    """
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
