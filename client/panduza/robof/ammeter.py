from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn
from hamcrest import assert_that, equal_to, any_of, has_item

class KeywordsAmmeter(object):

    ###########################################################################
    # DIRECTION
    ###########################################################################

    @keyword
    def read_ammeter_measure(self, amm_alias:str):
        """
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        return pza[amm_alias].measure.value.get()

    # ---

    @keyword
    def set_ammeter_measure_polling_cycle(self, amm_alias:str, cycle:float, ensure=True):
        """Set the state polling cycle
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[amm_alias].measure.polling_cycle.set(float(cycle), ensure)

    ###########################################################################
    # FULL STANDART TESTS
    ###########################################################################

    @keyword
    def test_basic_access_of_ammeter_interface(self, amm_alias:str):
        """Just test basic commands of a ammeter interface
        """
        #
        BuiltIn().run_keyword("Set Ammeter Measure Polling Cycle", amm_alias, 0.5)
        BuiltIn().run_keyword("Sleep", 1)

        measure = BuiltIn().run_keyword("Read Ammeter Measure", amm_alias)
        BuiltIn().run_keyword("Should Be True", measure != None)

        BuiltIn().run_keyword("Set Ammeter Measure Polling Cycle", amm_alias, 3)

