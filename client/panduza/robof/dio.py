from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn

class KeywordsDio(object):


    ###########################################################################
    # DIRECTION Value
    ###########################################################################

    @keyword
    def set_direction_value(self, dio_alias, direction, ensure=True):
        """Set the direction value
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].direction.value.set(float(direction), ensure)
    
    @keyword
    def set_direction_pull(self, dio_alias, pull, ensure=True):
        """Set the direction pull
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].direction.pull.set(float(pull), ensure)

    @keyword
    def set_direction_polling_cycle(self, dio_alias:str, cycle:float, ensure=True):
        """Set the direction polling cycle
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].direction.polling_cycle.set(float(cycle), ensure)


    ###########################################################################
    # State
    ###########################################################################

    @keyword
    def set_state_active(self, dio_alias, active, ensure=True):
        """Set the state active
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].state.active.set(bool(active), ensure)

    @keyword
    def set_state_active_low(self, dio_alias, active_low, ensure=True):
        """Set the state active low
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].state.active_low.set(bool(active_low), ensure)
        
    @keyword
    def set_state_polling_cycle(self, dio_alias:str, cycle:float, ensure=True):
        """Set the state polling cycle
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].state.polling_cycle.set(float(cycle), ensure)