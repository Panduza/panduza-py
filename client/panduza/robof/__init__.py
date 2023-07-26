from robotlibcore import DynamicCore, keyword

from robot.libraries.BuiltIn import BuiltIn

from ..core.core import Core

from .ammeter       import KeywordsAmmeter
from .client        import KeywordsClient
from .bps           import KeywordsBps
from .dio           import KeywordsDio
from .relay         import KeywordsRelay
from .voltmeter     import KeywordsVoltmeter

from .tool_chart    import KeywordsToolChart


from ..interfaces.generator import GenerateAllInterfacesFromAliases

class Keywords(DynamicCore):

    def __init__(self):
        libraries = [
            KeywordsAmmeter(),
            KeywordsClient(),
            KeywordsDio(),
            KeywordsBps(),
            KeywordsRelay(),
            KeywordsVoltmeter(),

            KeywordsToolChart()
        ]
        DynamicCore.__init__(self, libraries)

    @keyword
    def load_pza_interfaces_from_aliases(self, connections):
        """
        """
        interfaces = GenerateAllInterfacesFromAliases(connections=connections)
        # print(interfaces)

        BuiltIn().set_suite_variable("${__pza__}", interfaces)

