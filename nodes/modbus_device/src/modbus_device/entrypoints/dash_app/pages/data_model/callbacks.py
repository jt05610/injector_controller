from dash import Output, Input, ctx, callback, Dash, html

from modbus_device import bootstrap
from modbus_device.domain import commands

bus = bootstrap.bootstrap()


class Callbacks:
    last_n_clicks = 0

    @classmethod
    def create_data_model(cls, n_clicks, ref, di, coils, ir, hr):
        print("aaa")
        if n_clicks != cls.last_n_clicks:
            print("aaa")
            cmd = commands.CreateDataModel(
                ref=ref,
                discrete_inputs=(d.strip(" ") for d in di.split(",")),
                coils=(coil.strip(" ") for coil in coils.split(",")),
                input_registers=(r.strip(" ") for r in ir.split(",")),
                holding_registers=(r.strip(" ") for r in hr.split(",")),
            )
            bus.handle(cmd)
            cls.last_n_clicks = n_clicks


def attach(app: Dash):
    app.callback(
        Output("data-model-table", "children"),
        Input("data-model-create-btn", "n_clicks"),
        Input("data-model-ref", "value"),
        Input("data-model-discrete-inputs", "value"),
        Input("data-model-coils", "value"),
        Input("data-model-input-registers", "value"),
        Input("data-model-holding-registers", "value"),
    )(Callbacks.create_data_model)
