import asyncio
from meta_drivers.ammeter import MetaDriverAmmeter


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

        settings = tree.get("settings", {})
        # self.log.info(settings)

        # work_with_fake_psu = settings.get("work_with_fake_psu", None)
        # self.psu_obj = self.get_interface_instance_from_pointer(work_with_fake_psu)

        
        self.__task_increment = loop.create_task(self.__increment_task())


        self.__fakes = {
            "measure": {
                "value": 0
            }
        }

        # Call meta class PSU ini
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    async def _PZA_DRV_AMMETER_read_measure_value(self):
        return self.__fakes["measure"]["value"]

    # ---

    async def __increment_task(self):
        while True:
            await asyncio.sleep(0.2)
            self.__fakes["measure"]["value"] += 0.001
