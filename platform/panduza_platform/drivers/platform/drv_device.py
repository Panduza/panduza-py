import time
from core.platform_driver import PlatformDriver
import sys

class DriverDevice(PlatformDriver):
    """
    """

    ###########################################################################
    ###########################################################################

    def _PZA_DRV_config(self):
        """From PlatformDriver
        """
        return {
            "name": "py.device",
            "description": "Generic device interface",
            "info": {
                "type": "device",
                "version": "0.0"
            }
        }

    ###########################################################################
    ###########################################################################

    async def _PZA_DRV_loop_init(self, loop, tree):
        """From PlatformDriver
        """

        print("DriverDevice: _PZA_DRV_loop_init", self.device)
        await self._update_attributes_from_dict({
            "identify": {
                "model": self.device._model,
                "manufacturer": self.device._manufacturer,
            }
        })

        # Tell the platform that the init state end sucessfuly
        self._PZA_DRV_init_success()


