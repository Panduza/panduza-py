from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn
from hamcrest import assert_that, equal_to, any_of, has_item

class KeywordsDio(object):

    ###########################################################################
    # DIRECTION
    ###########################################################################

    @keyword
    def set_dio_direction(self, dio_alias, direction, ensure=True):
        """Set DIO direction
        """
        assert_that( ["in", "out"], has_item(direction) )
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].direction.value.set(direction, ensure)

    @keyword
    def set_dio_internal_resistor(self, dio_alias, pull, ensure=True):
        """Set the DIO internal resistor
        """
        assert_that( ["up", "down", "open"], has_item(pull) )
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].direction.pull.set(pull, ensure)

    # @keyword
    # def set_direction_polling_cycle(self, dio_alias:str, cycle:float, ensure=True):
    #     """Set the direction polling cycle
    #     """
    #     pza = BuiltIn().get_variable_value("${__pza__}")
    #     pza[dio_alias].direction.polling_cycle.set(float(cycle), ensure)

    ###########################################################################
    # State
    ###########################################################################

    @keyword
    def set_dio_state(self, dio_alias, state, ensure=True):
        """
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].state.active.set(bool(state), ensure)

    @keyword
    def change_dio_logic_active_low(self, dio_alias, active_low, ensure=True):
        """Set the state active low
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].state.active_low.set(bool(active_low), ensure)

    # @keyword
    # def set_state_polling_cycle(self, dio_alias:str, cycle:float, ensure=True):
    #     """Set the state polling cycle
    #     """
    #     pza = BuiltIn().get_variable_value("${__pza__}")
    #     pza[dio_alias].state.polling_cycle.set(float(cycle), ensure)

    ###########################################################################
    # FULL STANDART TESTS
    ###########################################################################

    @keyword
    def test_basic_access_of_dio_interface(self, dio_alias):
        """Just test basic commands of a DIO interface
        """
        # Test voltage goal
        BuiltIn().run_keyword("Set Dio Direction", dio_alias, "in")
        BuiltIn().run_keyword("Set Dio Direction", dio_alias, "out")

        BuiltIn().run_keyword("Set Dio Internal Resistor", dio_alias, "up")
        BuiltIn().run_keyword("Set Dio Internal Resistor", dio_alias, "down")
        BuiltIn().run_keyword("Set Dio Internal Resistor", dio_alias, "open")

        BuiltIn().run_keyword("Set Dio State", dio_alias, True)
        BuiltIn().run_keyword("Set Dio State", dio_alias, False)

        BuiltIn().run_keyword("Change dio logic active low", dio_alias, True)
        BuiltIn().run_keyword("Change dio logic active low", dio_alias, False)

