from hamcrest import assert_that, has_key, instance_of
from panduza_platform.meta_drivers.ammeter import MetaDriverAmmeter
from panduza_platform.connectors.modbus_client_serial import ConnectorModbusClientSerial

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

    async def _PZA_DRV_loop_init(self, loop, tree):
        """Driver initialization
        """

        # Load settings
        assert_that(tree, has_key("settings"))
        settings = tree["settings"]
        assert_that(settings, instance_of(dict))

        # Checks
        assert_that(settings, has_key("usb_vendor"))
        assert_that(settings, has_key("usb_model"))
        assert_that(settings, has_key("serial_baudrate"))

        # Get the gate
        self.modbus = await ConnectorModbusClientSerial.Get(**settings)

        # 
        self.modbus_unit = 1

        # Call meta class PSU ini
        await super()._PZA_DRV_loop_init(loop, tree)


    ###########################################################################
    ###########################################################################


    # AMPS #


    async def _PZA_DRV_AMPERMT_read_value(self):
        addr = 0x0011
        regs = self.modbus.read_holding_registers(addr, 1, self.modbus_unit)
        self.log.debug(f"read real amps addr={hex(addr)} regs={regs}")
        float_value = float(regs[0]) / 1000.0
        return float_value


