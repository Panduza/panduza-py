import abc

class PlatformDeviceModel:
    """Mother class for device models
    """

    def __init__(self, settings = {}) -> None:
        """Constructor
        """
        self._initial_settings = settings

    @abc.abstractmethod
    def _PZA_DEV_config(self):
        """
        """
        pass

    @abc.abstractmethod
    def _PZA_DEV_interfaces(self):
        """
        """
        return {}

