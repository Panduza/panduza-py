from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn
from hamcrest import assert_that, equal_to, any_of
from .utils import boolean_str_to_boolean

class KeywordsDio(object):


    ###########################################################################
    # DIRECTION Value
    ###########################################################################

    @keyword
    def set_direction_value(self, dio_alias, direction, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].direction.value.set(float(direction), ensure)

    def set_direction_pull(self, dio_alias, pull, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].direction.pull.set(float(pull), ensure)
    @keyword
    def set_direction_polling_cycle(self, dio_alias:str, cycle:float, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].direction.polling_cycle.set(float(cycle), ensure)

    ###########################################################################
    # State
    ###########################################################################

    @keyword
    def set_state_active(self, dio_alias, active, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].state.active.set(bool(active), ensure)

    def set_state_active_low(self, dio_alias, active_low, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].state.active_low.set(bool(active_low), ensure)

    @keyword
    def set_state_polling_cycle(self, dio_alias:str, cycle:float, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].state.polling_cycle.set(float(cycle), ensure)