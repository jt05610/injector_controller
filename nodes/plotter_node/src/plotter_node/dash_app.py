import json
from collections import deque

from dash import Dash, html, dcc
from dash.dependencies import Output, Input
import plotly
import plotly.graph_objs as go
import redis
import time

app = Dash(__name__)

xs = [0]
ys = [0]

HOSTNAME = "127.0.0.1"
PORT = 6379

client = redis.Redis(
    host=HOSTNAME,
    port=PORT
)

pubsub = client.pubsub(ignore_subscribe_messages=True)

pubsub.subscribe("modbus.input_registers.read.res")


@app.callback(Output('live-graph', 'figure'),
              (Input('graph-update', 'n_intervals')))
def update_graph(n):
    client.publish("modbus.input_registers.read.req", "1 0 1")
    m = next(pubsub.listen())
    data = json.loads(m["data"])
    if m["channel"] == b"modbus.input_registers.read.res":
        ys.append(data)
    xs.append(n)
    data = go.Scatter(
        x=xs,
        y=ys,
        name='Scatter',
        mode='lines+markers'
    )
    return {
        'data': [data],
        'layout': go.Layout(xaxis=dict(range=[min(xs), max(xs)]),
                            yaxis=dict(range=[min(ys), max(ys)])
                            )
    }


def setup_app():
    app.layout = html.Div(
        (
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(id='graph-update', interval=1000, n_intervals=0),
        )
    )


def add_data(data: str):
    ys.append(data)


def app_thread():
    setup_app()
    app.run(debug=True)


if __name__ == "__main__":
    client.publish("modbus.coil.write.req", "1 0 1")
    app_thread()
