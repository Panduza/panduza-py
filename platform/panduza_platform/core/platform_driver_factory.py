import traceback
from .platform_errors import InitializationError

from drivers import PZA_DRIVERS_LIST as INBUILT_DRIVERS

class PlatformDriverFactory:
    """Manage the factory of drivers
    """

    # ---

    def __init__(self, parent_platform):
        """ Constructor
        """
        self.__drivers = {}
        self.__platform = parent_platform
        self.__log = self.__platform.log

    # ---

    def produce_interface(self, bench_name, device_name, interface_config):
        """
        """
        try:
            name = interface_config["name"]
            driver_name = interface_config["driver"]

            # Control the driver exists in the database
            if not driver_name in self.__drivers:
                raise InitializationError(f"\"{driver_name}\" is not found in this platform (required by \"{bench_name}/{device_name}\")")

            driver_obj = self.__drivers[driver_name] 

            instance = driver_obj()
            instance.set_platform(self.__platform)
            instance.set_bench_name(bench_name)
            instance.set_device_name(device_name)
            instance.set_tree(interface_config)

            self.__log.info(f"> {name} [{driver_name}]")

        except Exception as e:
            self.__log.error(f"{driver_name} : {name} ({str(e)}) --- {traceback.format_exc()}")


        return instance

    # ---

    def discover(self):
        """Find device models managers
        """
        self.__log.info(f"=")
        for drv in INBUILT_DRIVERS:
            self.register_driver(drv)

    # ---

    def register_driver(self, dev):
        """Register a new driver
        """
        try:

            # Debug
            # self.__log.debug(f"Try to register driver: '{dev}'")

            # Extract config
            dev_config = dev()._PZA_DRV_config()

            # Control
            if not 'name' in dev_config:
                raise InitializationError(f"'name' field is not found in config of driver {dev} => config:{dev_config}")

            # Register driver
            name = dev()._PZA_DRV_config()['name']
            self.__drivers[name] = dev
            self.__log.info(f"Register driver: '{name}'")

        except NotImplementedError as e:
            raise InitializationError(f"Driver {dev} bad implementation: {e}")
