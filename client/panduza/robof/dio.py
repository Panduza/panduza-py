from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn
from hamcrest import assert_that, equal_to, any_of, has_item

class KeywordsDio(object):


    ###########################################################################
    # DIRECTION
    ###########################################################################

    @keyword
    def set_dio_direction(self, dio_alias, direction, ensure=True):
        """Set direction
        """
        assert_that( ["in", "out"], has_item(direction) )
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[dio_alias].direction.value.set(direction, ensure)

    @keyword
    def set_direction_pull(self, dio_alias, pull, ensure=True):
        """Set the direction pull
        """
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

    # @keyword
    # def set_state_active(self, dio_alias, active, ensure=True):
    #     """Set the state active
    #     """
    #     pza = BuiltIn().get_variable_value("${__pza__}")
    #     pza[dio_alias].state.active.set(bool(active), ensure)

    # @keyword
    # def set_state_active_low(self, dio_alias, active_low, ensure=True):
    #     """Set the state active low
    #     """
    #     pza = BuiltIn().get_variable_value("${__pza__}")
    #     pza[dio_alias].state.active_low.set(bool(active_low), ensure)
        
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
        # BuiltIn().run_keyword("Set Power Supply Voltage Goal", psu_alias, 3.3)

        # # Test current limit
        # BuiltIn().run_keyword("Set Power Supply Current Goal", psu_alias, 2)
        # BuiltIn().run_keyword("Set Power Supply Current Goal", psu_alias, 0.1)

        # # Try to turn on and off
        # BuiltIn().run_keyword("Turn On Power Supply", psu_alias)
        # BuiltIn().run_keyword("Power Supply Should Be", psu_alias, "on")
        # BuiltIn().run_keyword("Turn Off Power Supply", psu_alias)
        # BuiltIn().run_keyword("Power Supply Should Be", psu_alias, "off")

        # BuiltIn().run_keyword("Turn Power Supply", psu_alias, "on")
        # BuiltIn().run_keyword("Power Supply Should Be", psu_alias, "on")
        # BuiltIn().run_keyword("Turn Power Supply", psu_alias, "off")
        # BuiltIn().run_keyword("Power Supply Should Be", psu_alias, "off")
        pass


