from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from src import klant_alarm_overzicht
from . import ids


def render(app: Dash) -> html.Div:
    all_klanten = klant_alarm_overzicht.ALARM_DATA['index']

    @app.callback(
        Output(ids.KLANT_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_KLANT_BUTTON, "n_clicks"),
    )
    def select_all_klanten(_: int) -> list[str]:
        return all_klanten

    @app.callback(
        Output(ids.KLANT_DROPDOWN, "value"),
        Input(ids.SELECT_TOP_FIVE_KLANT_BUTTON, "n_clicks"),
    )
    def select_top_five_klanten(_: int) -> list[str]:
        return all_klanten[:5]

    @app.callback(
        Output(ids.KLANT_DROPDOWN, "value"),
        Input(ids.SELECT_TOP_TEN_KLANT_BUTTON, "n_clicks"),
    )
    def select_top_ten_klanten(_: int) -> list[str]:
        return all_klanten[:10]

    return html.Div(
        children=[
            html.H4("Klant"),
            # dcc.Input(
            #     type="datetime-local",
            #     step="1",
            #     id=ids.SELECT_FROM_TIME
            # ),
            dcc.Dropdown(
                id=ids.KLANT_DROPDOWN,
                options=[{"label": klant, "value": klant} for klant in all_klanten],
                value=[],
                multi=True,
            ),
            html.Hr(),
            html.Button(
                className="dropdown-button",
                children=["Selecteer alle"],
                id=ids.SELECT_ALL_KLANT_BUTTON,
                n_clicks=0,
            ),
            html.Button(
                className="dropdown-button",
                children=["Top 5"],
                id=ids.SELECT_TOP_FIVE_KLANT_BUTTON,
                n_clicks=0,
            ),
            html.Button(
                className="dropdown-button",
                children=["Top 10"],
                id=ids.SELECT_TOP_TEN_KLANT_BUTTON,
                n_clicks=0,
            )

        ]
    )
