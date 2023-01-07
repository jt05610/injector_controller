from modbus_device.entrypoints.dash_app import server
from modbus_device.entrypoints.dash_app.pages.data_model.callbacks import (
    attach as dm_attach,
)

if __name__ == "__main__":
    dm_attach(server.get_app())
    server.run(debug=True)
