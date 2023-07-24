import time
from core.platform_driver import PlatformDriver

class DriverPlatform(PlatformDriver):
    """
    """

    ###########################################################################
    ###########################################################################

    def _PZA_DRV_config(self):
        """From PlatformDriver
        """
        return {
            "name": "py.platform",
            "description": "Platform driver for python platform",
            "info": {
                "type": "platform",
                "version": "0.0"
            }
        }

    ###########################################################################
    ###########################################################################

    async def _PZA_DRV_loop_init(self, loop, tree):
        """From PlatformDriver
        """
        # Update the number of managed interface
        await self._update_attribute("info", "interfaces", self.platform.get_interface_number())

        # Tell the platform that the init state end sucessfuly
        self._PZA_DRV_init_success()

