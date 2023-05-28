from collections import ChainMap
from panduza_platform.meta_drivers.ampermt import MetaDriverAmpermt
from panduza_platform.connectors.modbus_client_serial import ConnectorModbusClientSerial
from panduza_platform.connectors.udev_tty import HuntUsbDevs


HM310T_USBID_VENDOR="1a86"
HM310T_USBID_MODEL="7523"
HM310T_TTY_BASE="/dev/ttyUSB"

STATE_VALUE_ENUM = { True : 1, False: 0  }
VOLTS_BOUNDS     = { "min": 0, "max": 30 }
AMPS_BOUNDS      = { "min": 0, "max": 10 }

def int_to_state_string(v_int):
    key_list = list(STATE_VALUE_ENUM.keys())
    val_list = list(STATE_VALUE_ENUM.values())
    position = val_list.index(v_int)
    return key_list[position]

class DriverHM310tAmpermeter(MetaDriverAmpermt):
    """
    """

    def _PZA_DRV_config(self):
        # Extend the common psu config
        return ChainMap(super()._PZA_DRV_config(), {
            "name": "Py_Ampermeter_HM310T",
            "description": "Ampermeter for HM310T channel",
            "compatible": [
                "hm310t.ampermeter",
                "hanmatek.hm310t.ampermeter",
                "psu.hanmatek.hm310t.ampermeter",
                "py.psu.hanmatek.hm310t.ampermeter"
            ]
        })

    # ---

    def __tgen(name_suffix):
        return {
            "name": "HM310T:" + name_suffix,
            "driver": "py.psu.hanmatek.hm310t"
        }

    # ---

    def _PZADRV_tree_template(self):
        return DriverHM310tAmpermeter.__tgen("template")

    # ---

    def _PZADRV_hunt_instances(self):
        instances = []
        usb_pieces = HuntUsbDevs(vendor=HM310T_USBID_VENDOR, model=HM310T_USBID_MODEL, subsystem="tty")
        for p in usb_pieces:
            instances.append(DriverHM310tAmpermeter.__tgen("instance"))
        return instances

    # ---

    def _PZADRV_loop_init(self, tree):
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
        super()._PZADRV_loop_init(tree)

    ###########################################################################
    ###########################################################################


    # AMPS #


    def _PZADRV_AMPERMT_read_value(self):
        addr = 0x0011
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read real amps addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 1000.0
        return float_value


