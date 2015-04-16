class OneWireException(Exception):
    pass


class AdapterError(OneWireException):
    pass


class DeviceError(OneWireException):
    pass


class CRCError(OneWireException):
    pass
