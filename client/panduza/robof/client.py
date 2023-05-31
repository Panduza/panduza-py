from panduza import Client

from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn




class KeywordsClient(object):

    @keyword
    def panduza_scan_server(self, addr, port):
        """
        """
        c = Client(url=addr, port=port)
        c.connect()
        return c.scan_interfaces()

