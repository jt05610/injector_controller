import dash
from dash import html
import dash_bootstrap_components as dbc


def topbar():
    return html.Div(
        (
            dbc.Nav(
                tuple(
                    dbc.NavLink(
                        (html.Div(page["name"], className="ms-2"),),
                        href=page["path"],
                        active="exact",
                    )
                    for page in dash.page_registry.values()
                    if page["path"].startswith("/data-model")
                ),
                vertical=False,
                pills=True,
            ),
        )
    )
