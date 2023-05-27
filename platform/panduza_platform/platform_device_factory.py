import abc



class PlatformDeviceModel:

    def _PZA_DEV_config(self):
        """
        """
        pass


    def _PZA_DEV_interfaces(self):
        """
        """
        return {}



class DevicePanduzaFakePsu(PlatformDeviceModel):

    def __init__(self, config = None):
        """ Constructor
        """
        pass

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "Panduza.FakePsu",
        }

    def _PZA_DEV_interfaces(self):
        """
        """
        return [
            {
                "name": "psu_1",
                "driver": "psu.fake"
            }
        ]



class PlatformDeviceFactory:
    """Manage the factory of devices
    """

    # ---

    def __init__(self, parent_platform):
        """ Constructor
        """
        self.__devices = {}
        self.__platform = parent_platform
        self.__log = self.__platform.log

    # ---

    def produce_device(self, config):
        model = config["model"]
        return self.__devices[model]()

    # ---

    def discover_available_devices(self):
        """Find device models managers
        """
        self.__log.info(f"=")
        self.register_device(DevicePanduzaFakePsu)
        self.__log.info(f"=")

    # ---

    def register_device(self, dev):
        """Register a new device model
        """
        model = dev()._PZA_DEV_config()['model']
        self.__log.info(f"Register device model: '{model}'")
        self.__devices[model] = dev


