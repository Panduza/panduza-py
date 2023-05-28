
from ...platform_device_model import PlatformDeviceModel


class DevicePanduzaFakePsu(PlatformDeviceModel):

    def __init__(self, config = None):
        """ Constructor
        """
        pass

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "Panduza.FakePsu",
        }

    def _PZA_DEV_interfaces(self):
        """
        """
        return [
            {
                "name": "psu_1",
                "driver": "panduza.fake.psu"
            }
        ]




