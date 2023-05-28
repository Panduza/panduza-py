import abc


class ConnectorModbusClientBase(metaclass=abc.ABCMeta):
    """Base class for modbus client connectors

    It defines method to interact with the modbus client
    """



    def write_register(self, address: int, value, unit: int = 1):
        """
        """
        pass

    @abc.abstractmethod
    def read_holding_registers(self, address: int, size: int = 1, unit: int = 1):
        pass


    def read_holding_registers(self, address: int, size: int = 1, unit: int = 1):
        """
        """
        pass
