from core.platform_device_model import PlatformDeviceModel

class DevicePanduzaFakeBps(PlatformDeviceModel):

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "Panduza.FakeBps",
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
                    "driver": "panduza.fake.bps"
                }
            )
            interfaces.append(
                {
                    "name": f"channel_{chan}_am",
                    "driver": "panduza.fake.ammeter",
                    "settings": {
                        "work_with_fake_bps": f"!//channel_{chan}"
                    }
                }
            )
            interfaces.append(
                {
                    "name": f"channel_{chan}_vl",
                    "driver": "panduza.fake.voltmeter",
                }
            )

        return interfaces



