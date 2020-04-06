
import dash
from dash.dependencies import Input, Output, State

import constants as const


def button_callbacks(app):
    """Contains most buttons callbacks

    Arguments:
        app {Dash.App} -- The app running
    """
    @app.callback([Output(f"{item}", 'active') for item in const.active_map],
                  [Input(f"{item}", 'n_clicks')for item in const.active_map],
                  [State(f"{item}", 'active') for item in const.active_map]
                  )
    def update_active_button(death, cases, iva, mobility, death_state, cases_state, iva_state, mobility_state):
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'mobility_map'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if not death and not cases and not iva:
            button_id = 'mobility_map'
            updating = [False, False, False, True]
        else:
            states = [death_state, cases_state, iva_state, mobility_state]
            updating = [False if button_id not in active else True for state,
                        active in zip(states, const.active_map)]

        return updating

    """This goes to all callbacks below

    Checks if the button was pressed and 
    then switches the current state of the button
    
    Returns:
        bool -- State of the button
    """
    @app.callback(Output("mobility_index", 'active'),
                  [Input("mobility_index", 'n_clicks')],
                  [State("mobility_index", 'active')])
    def change_mobility_visibility(mobility, mobility_active):
        if not mobility:
            return mobility_active

        return not mobility_active

    @app.callback(Output("ICU", 'active'),
                  [Input("ICU", 'n_clicks')],
                  [State("ICU", 'active')])
    def change_icu_visibility(icu, icu_active):
        if not icu:
            return icu_active
        return not icu_active

    @app.callback(Output("death", 'active'),
                  [Input("death", 'n_clicks')],
                  [State("death", 'active')])
    def change_icu_visibility(death, death_active):
        if not death:
            return death_active
        return not death_active

    @app.callback(Output("political", 'active'),
                  [Input("political", 'n_clicks')],
                  [State("political", 'active')])
    def change_icu_visibility(political, political_active):
        if not political:
            return political_active
        return not political_active

    @app.callback(Output("per_million", 'active'),
                  [Input("per_million", 'n_clicks')],
                  [State("per_million", 'active')])
    def change_icu_visibility(pm, pm_active):
        if not pm:
            return pm_active
        return not pm_active

    @app.callback(Output("confirmed", 'active'),
                  [Input("confirmed", 'n_clicks')],
                  [State("confirmed", 'active')])
    def change_icu_visibility(confirmed, confirmed_active):
        if not confirmed:
            return confirmed_active
        return not confirmed_active
