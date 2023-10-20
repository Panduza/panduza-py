from hamcrest import assert_that, has_key, instance_of
import asyncio
from meta_drivers.bpc import MetaDriverBpc
from connectors.serial_tty import SerialTty

VOLTAGE_BOUNDS     = { "min": 0, "max": 30 }
CURRENT_BOUNDS      = { "min": 0, "max": 5 }

def int_to_state_string(v_int):
    key_list = list(STATE_VALUE_ENUM.keys())
    val_list = list(STATE_VALUE_ENUM.values())
    position = val_list.index(v_int)
    return key_list[position]


COMMAND_TIME_LOCK=0.1


class DrvKoradKa3005pBPC(MetaDriverBpc):
    # =============================================================================
    # FROM MetaDriverBpc

    # ---

    def _PZA_DRV_BPC_config(self):
        """
        """
        return {
            "name": "korad.ka3005p.bpc",
            "description": "Power Supply KA3005P from Korad"
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
        assert_that(settings, has_key("serial_baudrate"))

        self.serial_connector = await SerialTty.Get(loop,**settings)
        
        # Call meta class BPC ini
        await super()._PZA_DRV_loop_init(loop, tree)

    ###########################################################################
    ###########################################################################

    async def _PZA_DRV_BPC_read_enable_value(self):
        # await asyncio.sleep(1)
        print("Sending cmd: {}".format("STATUS?"))
        await self.serial_connector.beg_cmd()
        await self.serial_connector.write_data("STATUS?", time_lock_s=COMMAND_TIME_LOCK)
        status = await self.serial_connector.read_data(n_bytes=1)
        print("LOL", status)
        await self.serial_connector.end_cmd()
        return bool(status[0] & (1 << 6))

    async def _PZA_DRV_BPC_write_enable_value(self, v):
        await self.serial_connector.beg_cmd()
        cmd = "OUT{}".format(int(v))
        print("Sending cmd: {}".format(cmd))
        await self.serial_connector.write_data(cmd, time_lock_s=COMMAND_TIME_LOCK)
        status = await self.serial_connector.read_data(n_bytes=1)
        await self.serial_connector.end_cmd()

    # ---

    async def _PZA_DRV_BPC_read_voltage_value(self):
        await self.serial_connector.beg_cmd()
        cmd = "VSET1?"
        await self.serial_connector.write_data(cmd, time_lock_s=COMMAND_TIME_LOCK)
        voltage = await self.serial_connector.read_data(n_bytes=5)
        return float(voltage)
        await self.serial_connector.end_cmd()

    async def _PZA_DRV_BPC_write_voltage_value(self, v):
        await self.serial_connector.beg_cmd()
        v = "{:05.2f}".format(v)
        cmd = "VSET1:{}".format(v)
        await self.serial_connector.write_data(cmd, time_lock_s=COMMAND_TIME_LOCK)
        await self.serial_connector.end_cmd()

    async def _PZA_DRV_BPC_voltage_value_min_max(self):
        return VOLTAGE_BOUNDS
    
    async def _PZA_DRV_BPC_read_voltage_decimals(self):
        return 2

    # ---

    async def _PZA_DRV_BPC_read_current_value(self):
        await self.serial_connector.beg_cmd()
        cmd = "ISET1?"
        await self.serial_connector.write_data(cmd, time_lock_s=COMMAND_TIME_LOCK)
        current = await self.serial_connector.read_data(n_bytes=5)
        await self.serial_connector.end_cmd()
        return float(current)

    async def _PZA_DRV_BPC_write_current_value(self, v):
        await self.serial_connector.beg_cmd()
        v = "{:05.3f}".format(v)
        cmd = "ISET1:{}".format(v)
        await self.serial_connector.write_data(cmd, time_lock_s=COMMAND_TIME_LOCK)
        await self.serial_connector.end_cmd()
        
    async def _PZA_DRV_BPC_current_value_min_max(self):
        return CURRENT_BOUNDS

    async def _PZA_DRV_BPC_read_current_decimals(self):
        return 3


