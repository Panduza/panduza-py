from dataclasses import dataclass
from ..core import Interface, Attribute, RoField, RwField

@dataclass
class Bpc(Interface):
    """Interface to manage power supplies
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

        # === ENABLE ===
        self.add_attribute(
            Attribute( name_ = "enable" )
        ).add_field(
            RwField( name_ = "value" )
        )

        # # === VOLTAGE ===
        # self.add_attribute(
        #     Attribute( name_ = "voltage" )
        # ).add_field(
        #     RoField( name_ = "real" )
        # ).add_field(
        #     RwField( name_ = "value" )
        # ).add_field(
        #     RoField( name_ = "min" )
        # ).add_field(
        #     RoField( name_ = "max" )
        # ).add_field(
        #     RoField( name_ = "decimals" )
        # ).add_field(
        #     RwField( name_ = "polling_cycle" )
        # )

        # # === CURRENT ===
        # self.add_attribute(
        #     Attribute( name_ = "current" )
        # ).add_field(
        #     RoField( name_ = "real" )
        # ).add_field(
        #     RwField( name_ = "value" )
        # ).add_field(
        #     RoField( name_ = "min" )
        # ).add_field(
        #     RoField( name_ = "max" )
        # ).add_field(
        #     RoField( name_ = "decimals" )
        # ).add_field(
        #     RwField( name_ = "polling_cycle" )
        # )

        # === SETTINGS ===
        self.add_attribute(
            Attribute( name_ = "settings", bypass_init_ensure = True )
        ).add_field(
            RwField( name_ = "ovp" )
        ).add_field(
            RwField( name_ = "ocp" )
        ).add_field(
            RwField( name_ = "silent" )
        )

        # === MISC ===
        self.add_attribute(
            Attribute( name_ = "misc", bypass_init_ensure = True  )
        )

        if self.ensure:
            self.ensure_init()


    def toggle(self):
        pass


    # Enable value need to be true or false to actually do something
    def turn_on(self):
        self.enable.value.set(True)

    def turn_off(self):
        self.enable.value.set(False)

    def is_on(self):
        return self.enable.value.get()
    
    # # Voltage get/set
    # def set_voltage_value(self, value):
    #     self.voltage.value.set(value)
    
    # def get_voltage_value(self):
    #     self.voltage.value.get()

    # # Current get/set
    # def set_current_value(self, value):
    #     self.current.value.set(value)
    
    # def get_current_value(self):
    #     self.current.value.get()