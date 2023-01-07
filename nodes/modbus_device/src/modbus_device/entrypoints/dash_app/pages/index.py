import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

from .side_bar import sidebar

dash.register_page(__name__, name="Data model", path="/", top_nav=True)


def layout():
    return dbc.Row(
        [
            dbc.Col(sidebar(), width=2),
            dbc.Col(html.Div(id="main-content"), width=10),
        ]
    )
