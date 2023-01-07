import dash
from dash import html
import dash_bootstrap_components as dbc


def sidebar():
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
                    if page.get("sidebar")
                ),
                vertical=True,
                pills=True,
            ),
        )
    )
