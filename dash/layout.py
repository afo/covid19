import dash
import dash_core_components as dcc
import dash_html_components as html

from extract_data import get_data


def generate_layout():
    layout = html.Div(children=[
        html.Div(className="app-header",
                 children=[html.Div("COVID19 Nordic Analysis", className="app-header--title")]),
        dcc.Tabs(children=[
            dcc.Tab(label="Total Deaths since March 10", id="Tab 1", children=[
                html.Div("Subheader", className="app-subheader"),
                checkboxes("1"),
                dcc.Graph(id="total_deaths")
            ]),
            dcc.Tab(label="Total Deaths per Mn inhabitants since March 10", id="Tab 2", children=[
                html.Div("Subheader", className="app-subheader"),
                checkboxes("2"),
                dcc.Graph(id="Deaths/mn")
            ]),
            dcc.Tab(label="Total Deaths, daily figures since day of first death", id="Tab 3", children=[
                html.Div("Subheader", className="app-subheader"),
                checkboxes("3"),
                dcc.Graph(id="daily_deaths")
            ]),
            dcc.Tab(label="Total Deaths per Mn inhabitants, daily figures since day of first death", id="Tab 4", children=[
                html.Div("Subheader", className="app-subheader"),
                checkboxes("4"),
                dcc.Graph("daily_deaths/mn")
            ])
        ]),
        html.Div(id="data", style={'display': 'none'}, children=get_data())
    ])
    return layout


def checkboxes(tab_name):
    options = [{
        'label': 'Sweden',
        'value': 'Sweden'
    },
        {
        'label': 'Finland',
        'value': 'Finland'
    },
        {
        'label': 'Norway',
        'value': 'Norway'
    },
        {
        'label': 'Denmark',
        'value': 'Denmark'
    },
        {
        'label': 'Iceland',
        'value': 'Iceland'
    }]
    value = ["Sweden", "Norway", "Finland", "Denmark", "Iceland"]
    checklist = dcc.Checklist(id=f"country_selection{tab_name}",
                              options=options, value=value, labelStyle={'display': 'inline-block'})
    return html.Div(children=[html.Label("Which countries"), checklist], style={'margin': 'auto'})

