from dataclasses import dataclass
from ..core import Interface, Attribute, RoField, RwField

@dataclass
class Blc(Interface):
    """Interface to manage Bench Laser Controller
    """

    interface:Interface = None

    def __post_init__(self):

        if self.alias:
            pass
        elif self.interface:
            # Build from an other interface
            self.alias = self.interface.alias
            self.addr = self.interface.addr
            self.port = self.interface.port
            self.topic = self.interface.topic
            self.client = self.interface.client

        super().__post_init__()

        # === MODE ===
        self.add_attribute(
            Attribute( name_ = "mode" )
        ).add_field(
            RwField( name_ = "value" )
        )

        # === ENABLE ===
        self.add_attribute(
            Attribute( name_ = "enable" )
        ).add_field(
            RwField( name_ = "value" )
        )

        # === POWER ===
        self.add_attribute(
            Attribute( name_ = "power" )
        ).add_field(
            RwField( name_ = "value" )
        ).add_field(
            RoField( name_ = "min" )
        ).add_field(
            RoField( name_ = "max" )
        ).add_field(
            RoField( name_ = "decimals" )
        )

        # === CURRENT ===
        self.add_attribute(
            Attribute( name_ = "current" )
        ).add_field(
            RwField( name_ = "value" )
        ).add_field(
            RoField( name_ = "min" )
        ).add_field(
            RoField( name_ = "max" )
        ).add_field(
            RoField( name_ = "decimals" )
        )

        if self.ensure:
            self.ensure_init()


    def toggle(self):
        pass


    # Enable value need to be true or false to actually do something
    def set_enable_value(self, value):
        self.enable.value.set(value)

    def get_enable_value(self):
        return self.enable.value.get()

    # Change mode at power or current
    def set_mode_constant_power(self):
        self.mode.value.set("constant_power")

    def set_mode_constant_current(self):
        self.mode.value.set("constant_current")

    # Set power value
    def set_power_goal_point(self, value):
        self.power.value.set(value)

    def get_power_min_value(self):
        return self.power.min.get()
        
    def get_power_max_value(self):
        return self.power.max.get()


