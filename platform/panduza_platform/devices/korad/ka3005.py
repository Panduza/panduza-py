
from core.platform_device import PlatformDevice

class DeviceKoradKA3005P(PlatformDevice):
    """Power Supply From Korad
    """

    def _PZA_DEV_config(self):
        """
        """
        return {
            "family": "BPS",
            "model": "KA3005P",
            "manufacturer": "Korad"
        }

    def _PZA_DEV_interfaces_generator(self):
        """
        """

        port = self.get_settings().get("serial_port")
        baudrate = 9600
        number_of_channel = 1

        interfaces = []
        for chan in range(0, number_of_channel):
            interfaces.append(
                {
                    "name": f":channel_{chan}:_ctrl",
                    "driver": "korad.ka3005p.bpc",
                    "settings": {
                        "serial_port_name": port,
                        "serial_baudrate": baudrate
                    }
                }
            )
            interfaces.append(
                {
                    "name": f":channel_{chan}:_vm",
                    "driver": "korad.ka3005p.voltmeter",
                    "settings": {
                        "serial_port_name": port,
                        "serial_baudrate": baudrate
                    }
                }
            )
            interfaces.append(
                {
                    "name": f":channel_{chan}:_am",
                    "driver": "korad.ka3005p.ammeter",
                    "settings": {
                        "serial_port_name": port,
                        "serial_baudrate": baudrate
                    }
                }
            )

        return interfaces



