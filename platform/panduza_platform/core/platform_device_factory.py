import traceback
from .platform_errors import InitializationError
from devices import PZA_DEVICES_LIST as INBUILT_DEVICES

class PlatformDeviceFactory:
    """Manage the factory of devices
    """

    # ---

    def __init__(self, parent_platform):
        """ Constructor
        """
        # The factory is composed of builders
        self.__device_templates = {}

        self.__platform = parent_platform
        self.__log = self.__platform.log

    # ---

    def produce_device(self, config):
        """Try to produce the device corresponding the ref
        """
        # Get ref and control it exists in the config provided by the user
        if not "ref" in config:
            raise InitializationError(f"Device \"ref\" field is not provided in the config {config}")
        ref = config["ref"]

        # Control the ref exists in the database
        if not ref in self.__device_templates:
            raise InitializationError(f"\"{ref}\" is not found in this platform")

        # 
        name = config.get("name", None)

        # Produce the device
        try:
            producted_device = self.__device_templates[ref](name, config.get("settings", {}))
            producted_device.initialize()
            return producted_device
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

    def register_device(self, device_builder):
        """Register a new device model
        """
        id = device_builder().get_ref()
        self.__log.info(f"Register device builder: '{id}'")
        self.__device_templates[id] = device_builder


