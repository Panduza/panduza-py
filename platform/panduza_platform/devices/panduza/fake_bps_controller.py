from core.platform_device import PlatformDevice

class DevicePanduzaFakeBps(PlatformDevice):

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "FakeBps",
            "manufacturer": "Panduza"
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
                    "driver": "panduza.fake.bpc"
                }
            )
            interfaces.append(
                {
                    "name": f"channel_{chan}_am",
                    "driver": "panduza.fake.ammeter",
                    "settings": {
                        "work_with_fake_bpc": f"!//channel_{chan}"
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



