import time
from ...platform_driver import PlatformDriver

class DriverPlatform(PlatformDriver):
    """
    """

    ###########################################################################
    ###########################################################################

    def _PZA_DRV_config(self):
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

    async def _PZA_DRV_loop_init(self, tree):

        # self.log.debug(f"{tree}")
        # self.log.debug(f">>>>>>>>>{len(self._platform.interfaces)}")

        
        # Update the number of managed interface
        self.number_of_interfaces = len(self._platform.interfaces)
        await self._update_attribute("info", "interfaces", self.number_of_interfaces)

        # Tell the platform that the init state end sucessfuly
        self._pzadrv_init_success()


    ###########################################################################
    ###########################################################################

    async def _PZADRV_loop_run(self):
        """
        """
        pass

    ###########################################################################
    ###########################################################################

    async def _PZADRV_loop_err(self):
        """
        """
        pass

    ###########################################################################
    ###########################################################################

    async def _PZADRV_cmds_set(self, payload):
        """From MetaDriver
        """
        pass

