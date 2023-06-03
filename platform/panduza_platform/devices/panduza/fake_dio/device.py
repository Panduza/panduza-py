

class DevicePanduzaFakeDio:

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
                "name": "io_1",
                "driver": "panduza.fake.psu"
            }
        ]

