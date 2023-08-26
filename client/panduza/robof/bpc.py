from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn
from hamcrest import assert_that, equal_to, any_of
from .utils import boolean_str_to_boolean

class KeywordsBpc(object):

    ###########################################################################
    # STATE
    ###########################################################################

    @keyword
    def turn_power_supply(self, bpc_alias, state, ensure=True):
        """Turn the bpc on the given state
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bpc_alias].enable.value.set(boolean_str_to_boolean(state), ensure)

    # ---

    @keyword
    def turn_on_power_supply(self, bpc_alias, ensure=True):
        """Turn on the bpc
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bpc_alias].enable.value.set(boolean_str_to_boolean("on"), ensure)

    # ---

    @keyword
    def turn_off_power_supply(self, bpc_alias, ensure=True, teardown=False):
        """Turn off the bpc
        """
        pza = BuiltIn().get_variable_value("${__pza__}")

        if pza == None:
            # It is ok if panduza is not initialized, only if in the teardown process
            assert not teardown
        else:
            pza[bpc_alias].enable.value.set(boolean_str_to_boolean("off"), ensure)

    # ---

    @keyword
    def power_supply_should_be(self, bpc_alias, state):
        """Check power supply state
        """
        expected_state_bool = boolean_str_to_boolean(state)
        pza = BuiltIn().get_variable_value("${__pza__}")
        read_state = pza[bpc_alias].enable.value.get()
        assert_that(read_state, equal_to(expected_state_bool))

    ###########################################################################
    # VOLTS
    ###########################################################################

    @keyword
    def set_power_supply_voltage_goal(self, bpc_alias, voltage, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bpc_alias].volts.goal.set(float(voltage), ensure)

    @keyword
    def set_power_supply_voltage_polling_cycle(self, bpc_alias:str, cycle:float, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bpc_alias].volts.polling_cycle.set(float(cycle), ensure)

    ###########################################################################
    # AMPS
    ###########################################################################

    @keyword
    def set_power_supply_current_goal(self, bpc_alias, current, ensure=True):
        """Set the power supply amps goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bpc_alias].amps.goal.set(float(current), ensure)

    @keyword
    def set_power_supply_current_polling_cycle(self, bpc_alias:str, cycle:float, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bpc_alias].amps.polling_cycle.set(float(cycle), ensure)

    ###########################################################################
    # SETTINGS
    ###########################################################################

    @keyword
    def turn_power_supply_ovp_setting(self, bpc_alias, value, ensure=True):
        """Turn bpc setting ovp to the given state
        """
        bool_val = boolean_str_to_boolean(value)
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bpc_alias].settings.ovp.set(bool_val, ensure)

    # ---

    @keyword
    def turn_power_supply_ocp_setting(self, bpc_alias, value, ensure=True):
        """Turn bpc setting ocp to the given state
        """
        bool_val = boolean_str_to_boolean(value)
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bpc_alias].settings.ocp.set(bool_val, ensure)

    # ---

    @keyword
    def turn_power_supply_silent_setting(self, bpc_alias, value, ensure=True):
        """Turn bpc setting silent to the given state
        """
        bool_val = boolean_str_to_boolean(value)
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bpc_alias].settings.silent.set(bool_val, ensure)

    ###########################################################################
    # MISC
    ###########################################################################

    @keyword
    def read_power_supply_misc(self, bpc_alias, misc_field, ensure=True):
        """Return the given misc_field
        """
        # assert_that(value, any_of(equal_to(True), equal_to(False)))
        pza = BuiltIn().get_variable_value("${__pza__}")
        return pza[bpc_alias].misc.get(misc_field)

    ###########################################################################
    # FULL STANDART TESTS
    ###########################################################################

    @keyword
    def interface_bpc_basic_controls(self, bpc_alias):
        """Just test basic commands of a Power SUpply interface

        Warning this test 
        """
        # Test voltage goal
        BuiltIn().run_keyword("Set Power Supply Voltage Goal", bpc_alias, 10)
        BuiltIn().run_keyword("Set Power Supply Voltage Goal", bpc_alias, 3.3)

        # Test current limit
        BuiltIn().run_keyword("Set Power Supply Current Goal", bpc_alias, 2)
        BuiltIn().run_keyword("Set Power Supply Current Goal", bpc_alias, 0.1)

        # Try to turn on and off
        BuiltIn().run_keyword("Turn On Power Supply", bpc_alias)
        BuiltIn().run_keyword("Power Supply Should Be", bpc_alias, "on")
        BuiltIn().run_keyword("Turn Off Power Supply", bpc_alias)
        BuiltIn().run_keyword("Power Supply Should Be", bpc_alias, "off")

        BuiltIn().run_keyword("Turn Power Supply", bpc_alias, "on")
        BuiltIn().run_keyword("Power Supply Should Be", bpc_alias, "on")
        BuiltIn().run_keyword("Turn Power Supply", bpc_alias, "off")
        BuiltIn().run_keyword("Power Supply Should Be", bpc_alias, "off")

