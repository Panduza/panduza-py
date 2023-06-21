from collections import ChainMap
from panduza_platform.meta_drivers.ammeter import MetaDriverAmmeter
from panduza_platform.connectors.modbus_client_serial import ConnectorModbusClientSerial
from panduza_platform.connectors.udev_tty import HuntUsbDevs



STATE_VALUE_ENUM = { True : 1, False: 0  }
VOLTS_BOUNDS     = { "min": 0, "max": 30 }
AMPS_BOUNDS      = { "min": 0, "max": 10 }

def int_to_state_string(v_int):
    key_list = list(STATE_VALUE_ENUM.keys())
    val_list = list(STATE_VALUE_ENUM.values())
    position = val_list.index(v_int)
    return key_list[position]

class DriverHM310tAmmeter(MetaDriverAmmeter):
    """
    """

    def _PZA_DRV_AMMETER_config(self):
        return {
            "name": "hanmatek.hm310t.ammeter",
            "description": "Ampermeter for HM310T channel"
        }

    # ---

    def _PZA_DRV_loop_init(self, loop, tree):
        """Driver initialization
        """
        # Load settings
        settings = dict() if "settings" not in tree else tree["settings"]
        settings["vendor"] = HM310T_USBID_VENDOR
        settings["model"] = HM310T_USBID_MODEL
        settings["base_devname"] = HM310T_TTY_BASE
        settings["baudrate"] = 9600

        # Get the gate
        self.modbus = ConnectorModbusClientSerial.GetV2(**settings)

        # 
        self.modbus_unit = 1

        # Misc
        self.__misc = {
            "model": "HM310T (Hanmatek)",
            "modbus_slave_id": self.modbus_unit
        }

        # Call meta class PSU ini
        super()._PZA_DRV_loop_init(tree)

    ###########################################################################
    ###########################################################################


    # AMPS #


    def _PZADRV_AMPERMT_read_value(self):
        addr = 0x0011
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read real amps addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 1000.0
        return float_value


