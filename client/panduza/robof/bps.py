from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn
from hamcrest import assert_that, equal_to, any_of
from .utils import boolean_str_to_boolean

class KeywordsBps(object):

    ###########################################################################
    # STATE
    ###########################################################################

    @keyword
    def turn_power_supply(self, bps_alias, state, ensure=True):
        """Turn the bps on the given state
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bps_alias].enable.value.set(boolean_str_to_boolean(state), ensure)

    # ---

    @keyword
    def turn_on_power_supply(self, bps_alias, ensure=True):
        """Turn on the bps
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bps_alias].enable.value.set(boolean_str_to_boolean("on"), ensure)

    # ---

    @keyword
    def turn_off_power_supply(self, bps_alias, ensure=True, teardown=False):
        """Turn off the bps
        """
        pza = BuiltIn().get_variable_value("${__pza__}")

        if pza == None:
            # It is ok if panduza is not initialized, only if in the teardown process
            assert not teardown
        else:
            pza[bps_alias].enable.value.set(boolean_str_to_boolean("off"), ensure)

    # ---

    @keyword
    def power_supply_should_be(self, bps_alias, state):
        """Check power supply state
        """
        expected_state_bool = boolean_str_to_boolean(state)
        pza = BuiltIn().get_variable_value("${__pza__}")
        read_state = pza[bps_alias].enable.value.get()
        assert_that(read_state, equal_to(expected_state_bool))

    ###########################################################################
    # VOLTS
    ###########################################################################

    @keyword
    def set_power_supply_voltage_goal(self, bps_alias, voltage, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bps_alias].volts.goal.set(float(voltage), ensure)

    @keyword
    def set_power_supply_voltage_polling_cycle(self, bps_alias:str, cycle:float, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bps_alias].volts.polling_cycle.set(float(cycle), ensure)

    ###########################################################################
    # AMPS
    ###########################################################################

    @keyword
    def set_power_supply_current_goal(self, bps_alias, current, ensure=True):
        """Set the power supply amps goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bps_alias].amps.goal.set(float(current), ensure)

    @keyword
    def set_power_supply_current_polling_cycle(self, bps_alias:str, cycle:float, ensure=True):
        """Set the power supply voltage goal
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bps_alias].amps.polling_cycle.set(float(cycle), ensure)

    ###########################################################################
    # SETTINGS
    ###########################################################################

    @keyword
    def turn_power_supply_ovp_setting(self, bps_alias, value, ensure=True):
        """Turn bps setting ovp to the given state
        """
        bool_val = boolean_str_to_boolean(value)
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bps_alias].settings.ovp.set(bool_val, ensure)

    # ---

    @keyword
    def turn_power_supply_ocp_setting(self, bps_alias, value, ensure=True):
        """Turn bps setting ocp to the given state
        """
        bool_val = boolean_str_to_boolean(value)
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bps_alias].settings.ocp.set(bool_val, ensure)

    # ---

    @keyword
    def turn_power_supply_silent_setting(self, bps_alias, value, ensure=True):
        """Turn bps setting silent to the given state
        """
        bool_val = boolean_str_to_boolean(value)
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[bps_alias].settings.silent.set(bool_val, ensure)

    ###########################################################################
    # MISC
    ###########################################################################

    @keyword
    def read_power_supply_misc(self, bps_alias, misc_field, ensure=True):
        """Return the given misc_field
        """
        # assert_that(value, any_of(equal_to(True), equal_to(False)))
        pza = BuiltIn().get_variable_value("${__pza__}")
        return pza[bps_alias].misc.get(misc_field)

    ###########################################################################
    # FULL STANDART TESTS
    ###########################################################################

    @keyword
    def interface_bps_basic_controls(self, bps_alias):
        """Just test basic commands of a Power SUpply interface

        Warning this test 
        """
        # Test voltage goal
        BuiltIn().run_keyword("Set Power Supply Voltage Goal", bps_alias, 10)
        BuiltIn().run_keyword("Set Power Supply Voltage Goal", bps_alias, 3.3)

        # Test current limit
        BuiltIn().run_keyword("Set Power Supply Current Goal", bps_alias, 2)
        BuiltIn().run_keyword("Set Power Supply Current Goal", bps_alias, 0.1)

        # Try to turn on and off
        BuiltIn().run_keyword("Turn On Power Supply", bps_alias)
        BuiltIn().run_keyword("Power Supply Should Be", bps_alias, "on")
        BuiltIn().run_keyword("Turn Off Power Supply", bps_alias)
        BuiltIn().run_keyword("Power Supply Should Be", bps_alias, "off")

        BuiltIn().run_keyword("Turn Power Supply", bps_alias, "on")
        BuiltIn().run_keyword("Power Supply Should Be", bps_alias, "on")
        BuiltIn().run_keyword("Turn Power Supply", bps_alias, "off")
        BuiltIn().run_keyword("Power Supply Should Be", bps_alias, "off")

