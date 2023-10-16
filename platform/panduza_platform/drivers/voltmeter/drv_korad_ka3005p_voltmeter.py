from hamcrest import assert_that, has_key, instance_of
import asyncio
from meta_drivers.voltmeter import MetaDriverVoltmeter
from connectors.serial_tty import ConnectorUartSerial


class DrvKoradKa3005pVoltmeter(MetaDriverVoltmeter):
    # =============================================================================
    # FROM MetaDriverVoltmeter

    def _PZA_DRV_VOLTMETER_config(self):
        """
        """
        return {
            "name": "korad.ka3005p.voltmeter",
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

        self.uart_connector = await ConnectorUartSerial.Get(loop,**settings)
        
        # Call meta class BPC ini
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    async def _PZA_DRV_VOLTMETER_read_measure_value(self):
        cmd = "VOUT1?"
        await self.uart_connector.write_uart(cmd)
        voltage = await self.uart_connector.read_uart(n_bytes=5)
        return float(voltage)

    # ---