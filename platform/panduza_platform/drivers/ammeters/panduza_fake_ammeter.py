from ...meta_drivers.ammeter import MetaDriverAmmeter


class DriverFakeAmmeter(MetaDriverAmmeter):
    """Fake Ammeter driver
    """

    # =============================================================================
    # FROM MetaDriverAmmeter

    def _PZA_DRV_AMMETER_config(self):
        return {
            "name": "panduza.fake.ammeter",
            "description": "Virtual AMMETER"
        }

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """Init function
        Reset fake parameters
        """

        self.__fakes = {
            "measure": {
                "value": 0
            }
        }

        # Call meta class PSU ini
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    def _PZADRV_AMMETER_read_measure_value(self):
        return self.__fakes["measure"]["value"]
