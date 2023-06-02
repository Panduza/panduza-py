
from .devices import PZA_DEVICES_LIST as INBUILT_DEVICES


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

    def discover(self):
        """Find device models managers
        """
        self.__log.info(f"=")
        for dev in INBUILT_DEVICES:
            self.register_device(dev)
        self.__log.info(f"=")

    # ---

    def register_device(self, dev):
        """Register a new device model
        """
        model = dev()._PZA_DEV_config()['model']
        self.__log.info(f"Register device model: '{model}'")
        self.__devices[model] = dev


