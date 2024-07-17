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

        # === ANALOG MODULATION ===
        self.add_attribute(
            Attribute( name_= "analog_modulation")
        ).add_field(
            RwField( name_= "value")
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

    ############################################################
    ######################### ENABLE ###########################
    ############################################################

    # Enable value need to be true or false to actually do something
    def turn_on(self):
        self.enable.value.set(True)

    def turn_off(self):
        self.enable.value.set(False)

    def is_on(self):
        return self.enable.value.get()

    ############################################################
    #################### ANALOG MODULATION #####################
    ############################################################

    # Enable value need to be true or false to actually do something
    def enable_analog_modulation(self):
        self.analog_modulation.value.set(True)

    def disable_analog_modulation(self):
        self.analog_modulation.value.set(False)

    def get_analog_modulation(self):
        return self.analog_modulation.value.get()
    
    ############################################################
    ########################## MODE ############################
    ############################################################

    # Change mode at power or current
    def set_mode_constant_power(self):
        self.mode.value.set("constant_power")

    def set_mode_constant_current(self):
        self.mode.value.set("constant_current")

    def get_mode(self):
        self.mode.value.get()

    ############################################################
    ########################## POWER ###########################
    ############################################################


    # Set power value directly with value
    def set_power(self, value):
        self.power.value.set(value)

    # Set power value with percentage (0% to 100%)
    def set_power_with_percentage(self, percentage):

        # I need to round the value because else the precision of the 
        # double could cause problem with too much decimals
        decimals_value = self.power.decimals.get()

        # Value given in mW
        value_with_percentage = round((1/100) * percentage * self.power.max.get(), int(decimals_value)) 
        self.power.value.set(value_with_percentage)
           
    def get_power_min(self):
        return self.power.min.get()
        
    def get_power_max(self):
        return self.power.max.get()
    
    def get_power(self):
        return self.power.value.get()

    def get_power_decimals(self):
        return self.power.decimals.get()
    

    ############################################################
    ######################## CURRENT ###########################
    ############################################################

    # Set power value directly with value
    def set_current(self, value):
        self.current.value.set(value)

    # Get functions

    def get_current(self):
        return self.current.value.get()

    def get_current_min(self):
        return self.current.min.get()
        
    def get_current_max(self):
        return self.current.max.get()

    def get_current_decimals(self):
        return self.current.decimals.get()