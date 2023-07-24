from core.platform_device_model import PlatformDeviceModel

class DevicePanduzaFakeRelayController(PlatformDeviceModel):

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "Panduza.FakeRelayController",
        }

    def _PZA_DEV_interfaces(self):
        """
        """

        number_of_channel = int( self._initial_settings.get("number_of_channel", 1) )

        interfaces = []
        for chan in range(0, number_of_channel):
            interfaces.append(
                {
                    "name": f"channel_{chan}",
                    "driver": "panduza.fake.relay"
                }
            )

        return interfaces



