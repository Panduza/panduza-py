
from ...platform_device_model import PlatformDeviceModel

class DevicePanduzaFakeDioController(PlatformDeviceModel):
    
    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "Panduza.FakeDioController",
        }

    def _PZA_DEV_interfaces(self):
        """
        """
        number_of_dio = self._initial_settings.get("number_of_dio", 1)
        interfaces = []
        for id in range(0, number_of_dio):
            interfaces.append(
                {
                    "name": f"dio_{id}",
                    "driver": "panduza.fake.dio"
                }
            )
        return interfaces


