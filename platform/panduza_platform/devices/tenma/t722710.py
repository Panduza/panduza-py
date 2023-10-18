
from core.platform_device import PlatformDevice

USBID_VENDOR="0416"
USBID_MODEL="5011"
TTY_BASE="/dev/ttyACM0"

class DeviceTenma722710(PlatformDevice):
    """Power Supply From Tenma
    """

    def _PZA_DEV_config(self):
        """
        """
        return {
            "family": "bps",
            "model": "722710",
            "manufacturer": "Tenma"
        }

    def _PZA_DEV_interfaces_generator(self):
        """
        """
        interfaces = []

        fake_mode = self.get_settings().get("fake_mode", False)


        if fake_mode:
            pass
        else:
            interfaces.append({
                "name": f":channel_{0}:_ctrl",
                "driver": "tenma.722710.bpc",
                "settings": {
                    "usb_vendor": USBID_VENDOR,
                    "usb_model": USBID_MODEL,
                    "serial_baudrate": 9600
                }
            })
            '''
            interfaces.append({
                "name": f"am",
                "driver": "tenma.722710.ammeter",
                "settings": {
                    "usb_vendor": USBID_VENDOR,
                    "usb_model": USBID_MODEL,
                    "serial_baudrate": 9600
                }
            })
	    '''
        return interfaces

