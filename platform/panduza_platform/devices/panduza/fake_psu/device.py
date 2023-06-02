
class DevicePanduzaFakePsu:

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

