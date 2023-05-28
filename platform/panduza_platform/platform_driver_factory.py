import traceback

from .inbuilt import PZA_DRIVERS_LIST as INBUILT_DRIVERS


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

            driver_obj = self.__drivers[driver_name] 

            instance = driver_obj()
            # instance.initialize(self, machine, broker, interface_config)
            #     self.interfaces.append({
            #         "name": name,
            #         "instance":instance
            #     })

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
        self.__log.info(f"=")

    # ---

    def register_driver(self, dev):
        """Register a new driver
        """
        name = dev()._PZA_DRV_config()['name']
        self.__log.info(f"Register driver: '{name}'")
        self.__drivers[name] = dev

