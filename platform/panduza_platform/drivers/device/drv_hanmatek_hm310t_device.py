import time
from hamcrest import assert_that, has_key, instance_of
from collections import ChainMap
from meta_drivers.bpc import MetaDriverDevice
from connectors.modbus_client_serial import ConnectorModbusClientSerial



class DrvHanmatekHm310tDevice(MetaDriverDevice):
    """ Driver to manage the HM310T power supply
    """

    # =============================================================================
    # FROM MetaDriverBpc

    # ---

    def _PZA_DRV_BPC_config(self):
        """
        """
        return {
            "name": "hanmatek.hm310t.device",
            "description": "Device HM310T from Hanmatek"
        }

    # ---

    def _PZA_DRV_loop_init(self, loop, tree):
        """Driver initialization
        """

        # Load settings
        assert_that(tree, has_key("settings"))
        settings = tree["settings"]
        assert_that(settings, instance_of(dict))

        # Checks
        assert_that(settings, has_key("vendor"))
        assert_that(settings, has_key("model"))
        assert_that(settings, has_key("baudrate"))

        # Get the gate
        self.modbus = ConnectorModbusClientSerial.Get(**settings)

        # 
        self.modbus_unit = 1

        # Misc
        self.__misc = {
            "model": "HM310T (Hanmatek)",
            "modbus_slave_id": self.modbus_unit
        }

        # Call meta class BPC ini
        super()._PZA_DRV_loop_init(tree)

