import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from ..side_bar import sidebar
from .top_bar import topbar

dash.register_page(__name__, name="Data model", top_nav=True, sidebar=True)


def content():
    return html.Div(
        children=(
            html.H2("Data model"),
            topbar(),
            html.Div(id="data-model-table"),
        )
    )


layout = dbc.Row(
    (
        dbc.Col(sidebar(), width=2),
        dbc.Col(content(), width=10),
    )
)
