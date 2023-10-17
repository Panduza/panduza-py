import abc

class SerialBase(metaclass=abc.ABCMeta):
    """Base class for modbus client connectors

    It defines method to interact with the modbus client
    """

    @abc.abstractmethod
    async def write_uart(self, message):
        """
        """
        pass

    @abc.abstractmethod
    async def read_uart(self):
        """
        """
        pass
