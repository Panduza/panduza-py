from hamcrest import assert_that, has_key, instance_of
import asyncio
from meta_drivers.bpc import MetaDriverBpc
from connectors.serial_tty import SerialTty

VOLTAGE_BOUNDS     = { "min": 0, "max": 30 }
CURRENT_BOUNDS      = { "min": 0, "max": 5 }

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
        await self.serial_connector.write_data("STATUS?", time_lock_s=COMMAND_TIME_LOCK)
        status = await self.serial_connector.read_data(n_bytes=1)
        return bool(status[0] & (1 << 6))

    async def _PZA_DRV_BPC_write_enable_value(self, v):
        await self.serial_connector.write_data("OUT{}".format(int(v)), time_lock_s=COMMAND_TIME_LOCK)

    # ---

    async def _PZA_DRV_BPC_read_voltage_value(self):
        await self.serial_connector.write_data("VSET1?", time_lock_s=COMMAND_TIME_LOCK)
        voltage = await self.serial_connector.read_data(n_bytes=5)
        return float(voltage)

    async def _PZA_DRV_BPC_write_voltage_value(self, v):
        await self.serial_connector.write_data("VSET1:{:05.2f}".format(v), time_lock_s=COMMAND_TIME_LOCK)

    async def _PZA_DRV_BPC_voltage_value_min_max(self):
        return VOLTAGE_BOUNDS
    
    async def _PZA_DRV_BPC_read_voltage_decimals(self):
        return 2

    # ---

    async def _PZA_DRV_BPC_read_current_value(self):
        await self.serial_connector.write_data("ISET1?", time_lock_s=COMMAND_TIME_LOCK)
        current = await self.serial_connector.read_data(n_bytes=6)
        return float(current[0:5])

    async def _PZA_DRV_BPC_write_current_value(self, v):
        await self.serial_connector.write_data("ISET1:{:05.3f}".format(v), time_lock_s=COMMAND_TIME_LOCK)
        
    async def _PZA_DRV_BPC_current_value_min_max(self):
        return CURRENT_BOUNDS

    async def _PZA_DRV_BPC_read_current_decimals(self):
        return 3


