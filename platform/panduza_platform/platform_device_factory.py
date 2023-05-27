import abc



class PlatformDevice:

    @abc.abstractmethod
    def _PZA_DEV_config(self):
        """
        """
        pass



class DevicePanduzaFakePsu(PlatformDevice):

    def __init__(self):
        """ Constructor
        """
        pass
    
    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "Panduza.FakePsu"
        }


class PlatformDeviceFactory:
    """Manage the factory of devices
    """

    # ---

    def __init__(self, logger):
        """ Constructor
        """
        self.devices = []
        self._log = logger

    # ---

    def register_device(self, dev):
        self._log.info(f"Register device: {dev()._PZA_DEV_config()['model']}")
        self.devices.append(dev)



