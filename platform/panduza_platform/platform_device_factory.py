import traceback
from .platform_errors import InitializationError
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
        """Try to produce the given device model
        """
        # Get model name and control it exists in the config provided by the user
        if not "model" in config:
            raise InitializationError(f"\"model\" field is not provided in the config {config}")
        model = config["model"]

        # Control the model exists in the database
        if not model in self.__devices:
            raise InitializationError(f"\"{model}\" is not found in this platform")

        # Produce the device
        try:
            return self.__devices[model](config.get("settings", {}))
        except Exception as e:
            raise InitializationError(f"{traceback.format_exc()}")

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


