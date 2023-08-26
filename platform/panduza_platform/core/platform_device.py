import abc
from .platform_errors import InitializationError

class PlatformDevice:
    """This class is a static and generic device builder
    It does not hold any attributes or members
    """

    def __init__(self, settings = {}) -> None:
        """Constructor
        """
        # Settings json provided by the user with the tree.json
        self._initial_settings = settings

    # ---

    def initialize(self):
        pass

    # ---

    def get_config_field(self, field):
        config = self._PZA_DEV_config()
        if not field in config:
            raise InitializationError(f"\"{field}\" field is not provided in the device builder config {config}")
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

    def get_model(self):
        return self.get_config_field("model")

    # ---

    def get_manufacturer(self):
        return self.get_config_field("manufacturer")

    # ---

    @abc.abstractmethod
    def _PZA_DEV_config(self):
        """
        """
        pass

    # ---

    @abc.abstractmethod
    def _PZA_DEV_interfaces(self):
        """
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

