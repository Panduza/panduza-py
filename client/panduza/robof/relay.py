from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn
from hamcrest import assert_that, equal_to, any_of

STATES_DICT= {
    "open": True, "close": False
}

class KeywordsRelay(object):

    ###########################################################################
    # DIRECTION
    ###########################################################################

    @keyword
    def set_relay_state(self, relay_alias:str, state):
        """
        """
        assert_that(state, any_of(equal_to("open"), equal_to("close")))
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[relay_alias].state.open.set(STATES_DICT[state])

    @keyword
    def get_relay_state(self, relay_alias:str):
        """
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        if pza[relay_alias].state.open.get():
            return True
        else:
            return False

    @keyword
    def open_relay(self, relay_alias:str):
        """
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[relay_alias].state.open.set(True)

    @keyword
    def close_relay(self, relay_alias:str):
        """
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[relay_alias].state.open.set(False)

    ###########################################################################
    # FULL STANDART TESTS
    ###########################################################################

    @keyword
    def test_basic_access_of_relay_interface(self, relay_alias:str):
        """Just test basic commands of a relay interface
        """
        #
        value = BuiltIn().run_keyword("Get Relay State", relay_alias)
        BuiltIn().run_keyword("Log", value)
        BuiltIn().run_keyword("Set Relay State", relay_alias, "open")
        BuiltIn().run_keyword("Sleep", 0.5)
        BuiltIn().run_keyword("Set Relay State", relay_alias, "close")
        BuiltIn().run_keyword("Sleep", 0.5)
        BuiltIn().run_keyword("Open Relay", relay_alias)
        BuiltIn().run_keyword("Sleep", 0.5)
        BuiltIn().run_keyword("Close Relay", relay_alias)
