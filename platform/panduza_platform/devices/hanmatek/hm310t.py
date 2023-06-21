
USBID_VENDOR="1a86"
USBID_MODEL="7523"
TTY_BASE="/dev/ttyUSB"

class DeviceHanmatekHm310t:
    """Power Supply From Hanmatek
    """

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "Hanmatek.Hm310t",
        }

    def _PZA_DEV_interfaces(self):
        """
        """
        interfaces = []

        fake_mode = self._initial_settings.get("fake_mode", False)


        if fake_mode:
            pass
        else:
            interfaces.append({
                "name": f"psu",
                "driver": "hanmatek.hm310t.psu",
                "settings": {
                    "vendor": USBID_VENDOR,
                    "model": USBID_MODEL,
                    "baudrate": 9600
                }
            })

        return interfaces

