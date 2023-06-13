import time
import inspect
from collections import ChainMap
from ..platform_driver import PlatformDriver

class MetaDriverAmmeter(PlatformDriver):
    """Abstract Driver with helper class to manage AmeperMeter interface
    """

    # =============================================================================
    # PLATFORM DRIVERS FUNCTIONS

    def _PZA_DRV_config(self):
        """Driver base configuration
        """
        base = {
            "info": {
                "type": "ammeter",
                "version": "0.0"
            }
        }
        return ChainMap(base, self._PZA_DRV_AMMETER_config())

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """From PlatformDriver
        """
        # Set handers
        self.__cmd_handlers = {
            "measure" : self.__handle_cmds_set_measure
        }

        # 
        self.__polling_cycle = 1

        # first update
        await self.__update_attribute_initial()

        # Init Success
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    async def _PZA_DRV_cmds_set(self, loop, payload):
        cmds = self.payload_to_dict(payload)
        # self.log.debug(f"cmds as json : {cmds}")
        for att in self.__cmd_handlers:
            if att in cmds:
                await self.__cmd_handlers[att](cmds[att])

    # =============================================================================
    # TO OVERRIDE IN DRIVER

    # ---

    def _PZA_DRV_AMMETER_config(self):
        """Driver base configuration
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    def _PZADRV_AMMETER_read_measure_value(self):
        """
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # =============================================================================
    # PRIVATE FUNCTIONS

    # ---

    async def __update_attribute_initial(self):
        """Function to perform the initial init
        """
        await self.__att_measure_full_update()

    # ---

    async def __handle_cmds_set_measure(self, cmd_att):
        """
        """
        update_obj = {}
        self._prepare_update(update_obj, 
                            "measure", cmd_att,
                            "polling_cycle", [float, int]
                            , self.__set_poll_cycle
                            , self.__get_poll_cycle)
        await self._update_attributes_from_dict(update_obj)

    # ---

    def __set_poll_cycle(self, v):
        self.__polling_cycle = v

    # ---

    def __get_poll_cycle(self):
        return self.__polling_cycle

    # ---

    async def __att_measure_full_update(self):
        """
        """
        await self._update_attributes_from_dict({
            "measure": {
                "value": self._PZADRV_AMMETER_read_measure_value(),
                "polling_cycle": self.__get_poll_cycle()
            }
        })

    # ---

