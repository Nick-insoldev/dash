from dash import Dash, html
from src import klant_alarm_overzicht, klant_dropdown,klant_alarm_type_overzicht


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1("Raportage tool"),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    klant_dropdown.render(app),
                ],
            ),
            klant_alarm_overzicht.render(app),
            klant_alarm_type_overzicht.render(app),
        ],
    )