import abc

class ConnectorBoundaryScanBase(metaclass=abc.ABCMeta):
    """Base class for boundary scan controller

    It defines method to interact with a boundary scan controller
    """


    async def read_number_of_devices(self):
        """
        """
        pass

    async def read_pin(self, device_number, pin):
        """
        """
        pass

    async def write_pin(self, device_number, pin, value):
        """
        """
        pass

