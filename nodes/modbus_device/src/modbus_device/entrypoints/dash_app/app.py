from dash import Dash, html, dash
import dash_bootstrap_components as dbc


class DashApp:
    def __init__(self):
        self.app = Dash(
            __name__,
            use_pages=True,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
        )

        self.app.layout = html.Div(
            children=(
                html.H1("Device"),
                dash.page_container,
            )
        )

    def get_app(self) -> Dash:
        return self.app

    def run(self, **kwargs):
        self.app.run(**kwargs)
