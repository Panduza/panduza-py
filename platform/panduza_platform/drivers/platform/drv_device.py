from core.platform_driver import PlatformDriver

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
            "info": {
                "number_of_interfaces": self.device.number_of_interfaces(),
            }
        })

        await self._update_attributes_from_dict({
            "identity": {
                "family": self.device.get_family(),
                "model": self.device.get_model(),
                "manufacturer": self.device.get_manufacturer(),
            }
        })

        # Tell the platform that the init state end sucessfuly
        self._PZA_DRV_init_success()


