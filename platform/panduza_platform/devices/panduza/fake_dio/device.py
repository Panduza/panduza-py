
from ....platform_device_model import PlatformDeviceModel

class DevicePanduzaFakeDio(PlatformDeviceModel):
    
    # FakeDioController ??

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "Panduza.FakeDio",
        }

    def _PZA_DEV_interfaces(self):
        """
        """
        
        
        return [
            {
                "name": "dio_1",
                "driver": "panduza.fake.dio"
            }
        ]

