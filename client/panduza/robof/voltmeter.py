from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn
from hamcrest import assert_that, equal_to, any_of, has_item

class KeywordsVoltmeter(object):

    ###########################################################################
    # DIRECTION
    ###########################################################################

    @keyword
    def read_voltmeter_measure(self, vlm_alias:str):
        """
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        return pza[vlm_alias].measure.value.get()

    # ---

    @keyword
    def set_voltmeter_measure_polling_cycle(self, vlm_alias:str, cycle:float, ensure=True):
        """Set the state polling cycle
        """
        pza = BuiltIn().get_variable_value("${__pza__}")
        pza[vlm_alias].measure.polling_cycle.set(float(cycle), ensure)

    ###########################################################################
    # FULL STANDART TESTS
    ###########################################################################

    @keyword
    def test_basic_access_of_voltmeter_interface(self, vlm_alias:str):
        """Just test basic commands of a voltmeter interface
        """
        #
        BuiltIn().run_keyword("Set Voltmeter Measure Polling Cycle", vlm_alias, 0.5)
        BuiltIn().run_keyword("Sleep", 1)
        BuiltIn().run_keyword("Read Voltmeter Measure", vlm_alias)
        BuiltIn().run_keyword("Set Voltmeter Measure Polling Cycle", vlm_alias, 3)

