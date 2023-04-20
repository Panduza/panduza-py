import time
from collections import ChainMap
from panduza_platform.meta_drivers.psu import MetaDriverPsu
from panduza_platform.connectors.modbus_client_serial import ConnectorModbusClientSerial

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

class DriverHM310T(MetaDriverPsu):
    """ Driver to manage the HM310T power supply
    """

    def _PZADRV_config(self):
        # Extend the common psu config
        return ChainMap(super()._PZADRV_config(), {
            "name": "Py_Psu_HM310T",
            "description": "Power Supply HM310T",
            "compatible": [
                "hm310t",
                "hanmatek.hm310t",
                "psu.hanmatek.hm310t",
                "py.psu.hanmatek.hm310t"
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
        return DriverHM310T.__tgen("template")

    # ---

    def _PZADRV_hunt_instances(self):
        instances = []
        usb_pieces = HuntUsbDevs(vendor=HM310T_USBID_VENDOR, model=HM310T_USBID_MODEL, subsystem="tty")
        for p in usb_pieces:
            instances.append(DriverHM310T.__tgen("instance"))
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

    # STATE #

    def _PZADRV_PSU_read_enable_value(self):
        addr = 0x0001
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read state addr={hex(addr)} regs={regs}")
        str_value = int_to_state_string(regs[0])
        return str_value

    # ---

    def _PZADRV_PSU_write_enable_value(self, v):
        addr = 0x0001
        int16_value = STATE_VALUE_ENUM[v]
        self.log.info(f"write state addr={hex(addr)} value={int16_value}")
        self.modbus.write_register(addr, int16_value, self.modbus_unit)

    # VOLTS #

    def _PZADRV_PSU_read_volts_goal(self):
        addr = 0x0030
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read goal volts addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 100.0
        return float_value

    # ---

    def _PZADRV_PSU_write_volts_goal(self, v):
        addr = 0x0030
        int16_value = int(v * 100)
        self.log.info(f"write goal volts addr={hex(addr)} valuex100={int16_value}")
        self.modbus.write_register(addr, int16_value, self.modbus_unit)

    # ---

    def _PZADRV_PSU_volts_goal_min_max(self):
        return VOLTS_BOUNDS

    # ---

    def _PZADRV_PSU_read_volts_real(self):
        addr = 0x0010
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read real volts addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 100.0
        return float_value

    # ---

    def _PZADRV_PSU_read_volts_decimals(self):
        return 2

    # AMPS #

    def _PZADRV_PSU_read_amps_goal(self):
        addr = 0x0031
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read goal amps addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 1000.0
        return float_value

    # ---

    def _PZADRV_PSU_write_amps_goal(self, v):
        addr = 0x0031
        int16_value = int(v * 1000.0)
        self.log.info(f"write goal amps addr={hex(addr)} valuex1000={int16_value}")
        self.modbus.write_register(addr, int16_value, self.modbus_unit)

    # ---

    def _PZADRV_PSU_amps_goal_min_max(self):
        return AMPS_BOUNDS

    # ---

    def _PZADRV_PSU_read_amps_real(self):
        addr = 0x0011
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read real amps addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 1000.0
        return float_value

    # ---

    def _PZADRV_PSU_read_amps_decimals(self):
        return 3

    # SETTINGS #

    def _PZADRV_PSU_settings_capabilities(self):
        return  {
            "ovp": False,
            "ocp": False,
            "silent": False,
        }

    # MISC #

    def _PZADRV_PSU_read_misc(self):
        return self.__misc

    # ---

    def _PZADRV_PSU_write_misc(self, field, v):
        # read only misc
        pass




