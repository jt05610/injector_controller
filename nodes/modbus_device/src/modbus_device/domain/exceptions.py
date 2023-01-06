from typing import Any, Union


class ValueOutOfRangeException(Exception):
    def __init__(self, value: int, max_value: int = 1):
        super(ValueOutOfRangeException, self).__init__(
            f"{value} is not in range (0, {max_value})."
        )


class WriteToReadOnlyException(Exception):
    def __init__(self, table_name: str):
        super(WriteToReadOnlyException, self).__init__(
            f"{table_name} is read only."
        )


class BadAddressPassedException(Exception):
    def __init__(self, address: Any):
        super(BadAddressPassedException, self).__init__(
            f"{address} is {type(address)} and should be either an int or str.",
        )


class AddressNotInTableException(Exception):
    def __init__(self, address: Union[str, int], table_name: Any):
        super(AddressNotInTableException, self).__init__(
            f"{address} is not an accessible address in {table_name}"
        )
