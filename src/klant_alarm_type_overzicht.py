import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from src import ids
from src import klant_alarm_overzicht
from src import mongodb as mongo

dftest=klant_alarm_overzicht.dftest
dftest=dftest.drop(columns=["_measurement","measurementName","endTime","_time"])





def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART_TYPE, "children"),
        [
            Input(ids.KLANT_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(nations: list[str]) -> html.Div:
        filtered_data = dftest.query("id in @nations")

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.BAR_CHART_TYPE)

        fig = px.bar(data_frame=filtered_data, color='fieldName',x='id', title="Calis klanten alarmen afgelopen 30d",
                    barmode='group')
        fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART_TYPE)

    return html.Div(id=ids.BAR_CHART_TYPE)