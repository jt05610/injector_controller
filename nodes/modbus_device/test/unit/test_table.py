import pytest
from modbus_device.domain.model import (
    discrete_inputs,
    coils,
    holding_registers,
    input_registers,
)
from modbus_device.domain.exceptions import (
    WriteToReadOnlyException,
    ValueOutOfRangeException,
    BadAddressPassedException,
    AddressNotInTableException,
)

NODE = 0xCC


@pytest.fixture()
def fake_discrete_inputs():
    return discrete_inputs(addresses=("fake_1", "fake_2"))


@pytest.fixture()
def fake_coils():
    return coils(addresses=("fake_1", "fake_2"))


@pytest.fixture()
def fake_input_registers():
    return input_registers(addresses=("fake_1", "fake_2"))


@pytest.fixture()
def fake_holding_registers():
    return holding_registers(addresses=("fake_1", "fake_2"))


@pytest.fixture()
def fake_tables(
    fake_discrete_inputs,
    fake_coils,
    fake_input_registers,
    fake_holding_registers,
):
    return (
        fake_discrete_inputs,
        fake_coils,
        fake_input_registers,
        fake_holding_registers,
    )


@pytest.fixture()
def fake_node_id():
    return NODE


@pytest.fixture()
def table_gen(fake_tables):
    yield (t for t in fake_tables)


@pytest.fixture()
def rw_table_gen(table_gen):
    yield (t for t in table_gen if not t.read_only)


@pytest.fixture()
def read_only_table_gen(table_gen):
    yield (t for t in table_gen if t.read_only)


def test_read(table_gen, fake_node_id):
    for table in table_gen:
        for address in range(len(table.addresses)):
            assert (
                table.read(node=fake_node_id, address=address)
                == f"{NODE} {address} {1 if table.read_code < 0x03 else 2}"
            )


def test_write_happy(rw_table_gen, fake_node_id):
    for table in rw_table_gen:
        for address in range(len(table.addresses)):
            value = 1 if table.write_code == 0x05 else 0xFFFFFFFF
            assert (
                table.write(node=fake_node_id, address=address, value=value)
                == f"{NODE} {address} {value}"
            )


def test_write_read_only(read_only_table_gen, fake_node_id):
    for table in read_only_table_gen:
        for address in range(len(table.addresses)):
            value = 50 * address
            with pytest.raises(WriteToReadOnlyException):
                table.write(node=fake_node_id, address=address, value=value)


def test_write_value_too_high(rw_table_gen, fake_node_id):
    for table in rw_table_gen:
        for address in range(len(table.addresses)):
            value = 2 if table.write_code == 0x05 else 0xFFFFFFFF1
            with pytest.raises(ValueOutOfRangeException):
                table.write(node=fake_node_id, address=address, value=value)


def test_bad_address_passed(fake_discrete_inputs):
    with pytest.raises(BadAddressPassedException):
        fake_discrete_inputs.read(0x01, Exception)


def test_address_not_in_table(fake_discrete_inputs):
    with pytest.raises(AddressNotInTableException):
        fake_discrete_inputs.read(0x01, "bad_address")
