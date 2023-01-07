import dash
from dash import html, dcc, callback, Input, Output, Dash
import dash_bootstrap_components as dbc

from ..side_bar import sidebar
from .top_bar import topbar

dash.register_page(__name__, top_nav=True)

_input = lambda label, _id, help_text: html.Div(
    [
        dbc.Label(label, html_for=_id),
        dbc.Input(id=_id),
        dbc.FormText(help_text, color="secondary"),
    ],
    className="mb-3",
)
form = dbc.Form(
    (
        _input(
            "Reference",
            "data-model-ref",
            "Enter a reference for the data model",
        ),
        _input(
            "Discrete inputs",
            "data-model-discrete-inputs",
            (
                "These are read only bitwise functions. "
                "Enter separated by a comma. Example: [btn_forward, btn_power]"
            ),
        ),
        _input(
            "Coils",
            "data-model-coils",
            (
                "These are read only bitwise functions. "
                "Enter separated by a comma. Example: [btn_forward, btn_power]"
            ),
        ),
        _input(
            "Input registers",
            "data-model-input-registers",
            (
                "These are read only 16-bit functions. "
                "Enter separated by a comma. "
                "Example: [get_reading, current_position]"
            ),
        ),
        _input(
            "Holding registers",
            "data-model-holding-registers",
            (
                "These are read/write 16-bit functions. "
                "Enter separated by a comma. "
                "Example: [calibrate_slope, target_positon]"
            ),
        ),
        dbc.Button(
            "Submit",
            id="data-model-create-btn",
            color="primary",
            n_clicks=0,
        ),
    )
)


def content():
    return html.Div(
        children=(
            html.H2("Data model"),
            topbar(),
            form,
        )
    )


layout = dbc.Row(
    (
        dbc.Col(sidebar(), width=2),
        dbc.Col(content(), width=10),
    )
)
