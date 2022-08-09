import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from src import ids


df = pd.read_csv("src/df.csv")
dftest=df.drop(columns=["result","_start","_stop","table","Unnamed: 0"])
# print(dftest['id'].unique())
# print(dftest[dftest.duplicated(['id'], keep=False)])
# print(dftest)
dftest = dftest[dftest.fieldName != "A_controle_online"]
aantal=dftest['id'].value_counts()
# print(aantal.columns())
ALARM_DATA=aantal.reset_index(name='count')
# aantal=pd.read_csv("aantal.csv")
# print(aantal.head())

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [
            Input(ids.KLANT_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(nations: list[str]) -> html.Div:
        filtered_data = ALARM_DATA.query("index in @nations")

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.BAR_CHART)

        fig = px.bar(data_frame=filtered_data, y='count', x='index', title="Calis klanten alarmen afgelopen 30d",
                     text_auto=True)

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)