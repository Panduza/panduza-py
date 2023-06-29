import abc

class ConnectorBoundaryScanBase(metaclass=abc.ABCMeta):
    """Base class for boundary scan controller

    It defines method to interact with a boundary scan controller
    """

    @abc.abstractmethod
    async def read_number_of_devices(self):
        """
        """
        pass

    @abc.abstractmethod
    async def get_idcode(self):
        """
        """
        pass

    @abc.abstractmethod
    async def read_pin(self, device_number, pin, direction):
        """
        """
        pass

    @abc.abstractmethod
    async def write_pin(self, device_number, pin, value):
        """
        """
        pass
