import abc
from .platform_errors import InitializationError

class PlatformDevice:
    """Represent a device

    It can be instanciated with empty settings to provide only the _PZA_DEV_config
    """

    def __init__(self, settings = {}) -> None:
        """Constructor
        """
        # Settings json provided by the user with the tree.json
        self.__settings = settings

        # Interfaces linked to this device
        self.__interfaces = []

    # ---

    def initialize(self):
        """Post initialization when the device is actually used
        """
        self.__interface_defs = self._PZA_DEV_interfaces_generator()

    # ---

    def register_interface(self, interface):
        self.__interfaces.append(interface)

    # ---

    def number_of_interfaces(self):
        return len(self.__interfaces)

    # ---

    def get_settings(self):
        """Return settings provided by the user for this device
        """
        return self.__settings

    # ---

    def get_interface_defs(self):
        return self.__interface_defs

    # ---

    def get_config_field(self, field):
        config = self._PZA_DEV_config()
        if not field in config:
            raise InitializationError(f"\"{field}\" field is not provided in the device config {config}")
        return config.get(field)

    # ---

    def get_ref(self):
        """Unique Identifier for this device model
        Different from the name that must be unique for each instance of this device
        """
        return self.get_manufacturer() + "." + self.get_model()

    # ---

    def get_name(self):
        """Unique Identifier for this device instance
        Return a function that can be overloaded by the device implementation to match specific needs
        """
        return self._PZA_DEV_unique_name_generator()

    # ---

    def get_base_name(self):
        return self.get_manufacturer() + "_" + self.get_model()

    # ---

    def get_family(self):
        return self.get_config_field("model")

    # ---

    def get_model(self):
        return self.get_config_field("model")

    # ---

    def get_manufacturer(self):
        return self.get_config_field("manufacturer")

    ###########################################################################
    ###########################################################################
    #
    # TO OVERRIDE IN SUBCLASS
    #
    ###########################################################################
    ###########################################################################

    @abc.abstractmethod
    def _PZA_DEV_config(self):
        """
        """
        pass

    # ---

    @abc.abstractmethod
    def _PZA_DEV_interfaces_generator(self):
        """Generate interface definitions from device settings
        """
        return {}

    # ---

    @abc.abstractmethod
    def _PZA_DEV_unique_name_generator(self):
        """Must provide a unique and determinist name for the new device

        By default this function does not support multiple instance of the same device on the smae bench.
        Because with this simple method, they will have the same name.
        """
        return self.get_base_name() 

