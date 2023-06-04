import abc
import json
import time
import inspect
from collections import ChainMap
from ..platform_driver import PlatformDriver

class MetaDriverDio(PlatformDriver):

    # =============================================================================
    # PLATFORM DRIVERS FUNCTIONS

    def _PZA_DRV_config(self):
        """Driver base configuration
        """
        base = {
            "info": {
                "type": "dio",
                "version": "0.0"
            }
        }
        return ChainMap(base, self._PZA_DRV_DIO_config())

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """From PlatformDriver
        """
        # Set handers
        # self.__cmd_handlers = {
        #     "direction" : self.__handle_cmd_set_direction_dio,
        #     "state" : self.__handle_cmd_set_state_dio,
        # }


        # # first update
        # self.__update_attribute_initial()
        
        # # polling cycle reset
        # start_time = time.perf_counter()
        # self.polling_ref = {
        #     "direction" : start_time,
        #     "state"  : start_time,
        # }

        # Init Success
        self._PZA_DRV_loop_init(loop, tree)

    # =============================================================================
    # TO OVERRIDE IN DRIVER

    # ---

    def _PZA_DRV_DIO_config(self):
        """Driver base configuration
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    def _PZADRV_DIO_get_direction_value(self):
        """ get value of direction value
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    def _PZADRV_DIO_set_direction_value(self, value):
        """ set value of direction value

        -  Args
            value : value to be set : in or out
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    def _PZADRV_DIO_get_direction_pull(self):
        """ get direction pull
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    def _PZADRV_DIO_set_direction_pull(self, v):
        """ set the pull direction
        -Args
        value : value to be set : up, down or open
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    def _PZADRV_DIO_get_state_active(self):
        """ get the active state
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    def _PZADRV_DIO_set_state_active(self,v):
        """ get the active state
        -Args
        value : value to be set : True or False
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    def _PZADRV_DIO_get_state_activeLow(self):
        """ get the active low state
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    def _PZADRV_DIO_set_state_activeLow(self,v):
        """ set the active low state
            -Args
            value : value to be set : True or False
        """
        raise NotImplementedError("Must be implemented !")

    # =============================================================================
    #


    # def _PZADRV_loop_run(self, loop):
    #     # polls
    #     # self.__poll_att_direction()
    #     # self.__poll_att_state()
    #     # time.sleep(0.1)
    #     pass

    # def _PZADRV_cmds_set(self, loop, payload):
    #     cmds = self.payload_to_dict(payload)
    #     self.log.debug(f"cmds as json : {cmds}")
    #     for att in self.__cmd_handlers:
    #         if att in cmds:
    #             self.__cmd_handlers[att](cmds[att])
    #     pass



    # def __poll_att_direction(self):

    #     polling_cycle = float(self._get_field("direction", "polling_cycle"))
        
    #     if polling_cycle < 0:
    #         return
    #     if (time.perf_counter() - self.polling_ref["direction"]) > polling_cycle:
    #         p = False
    #         p = self._update_attribute("direction", "pull", self._PZADRV_DIO_get_direction_pull(), False) or p
    #         p = self._update_attribute("direction", "value", self._PZADRV_DIO_get_direction_value(), False) or p
    #         if p:
    #             self._push_attribute("direction")
    #         self.polling_ref["direction"] = time.perf_counter()


    # def __poll_att_state(self):
        
    #     polling_cycle = float(self._get_field("state", "polling_cycle"))
    #     value = bool(self._get_field("state", "active"))
    #     if polling_cycle < 0:
    #         return
    #     if (time.perf_counter() - self.polling_ref["state"]) > polling_cycle:
    #         p = False
    #         p = self._update_attribute("state", "active", self._PZADRV_DIO_get_state_active(), False) or p
    #         p = self._update_attribute("state", "active_low", self._PZADRV_DIO_get_state_activeLow(), False) or p
    #         if p:
    #             self._push_attribute("state")
    #         self.polling_ref["state"] = time.perf_counter()


    # # first update
    # def __update_attribute_initial(self):

    #     # === direction
    #     d = False
    #     # /!\ 'or p' must be at the end
    #     d = self._update_attribute("direction", "value", self._PZADRV_DIO_get_direction_value(), False) or d
    #     d = self._update_attribute("direction", "pull", self._PZADRV_DIO_get_direction_pull(), False) or d
    #     d = self._update_attribute("direction", "polling_cycle", self._PZADRV_DIO_get_direction_polling_cycle(), False) or d
    #     if d:
    #         self._push_attribute("direction")

    #     # === state
    #     s = False
    #     s = self._update_attribute("state", "active", self._PZADRV_DIO_get_state_active(), False) or s
    #     s = self._update_attribute("state", "active_low", self._PZADRV_DIO_get_state_activeLow(), False) or s
    #     s = self._update_attribute("state", "polling_cycle", self._PZADRV_DIO_get_state_polling_cycle(), False) or s
    #     if s:
    #         self._push_attribute("state")



    # # update the direction attribut field
    # def __handle_cmd_set_direction_dio(self, cmd_att):
    #     # POLLING_CYCLE
    #     if "polling_cycle" in cmd_att:
    #         v = cmd_att["polling_cycle"]
    #         if not isinstance(v, int) and not isinstance(v, float):
    #             raise Exception(f"Invalid type for volts.polling_cycle {type(v)}")
    #         if v < 0:
    #             v = -1
    #         self._update_attribute("direction", "polling_cycle", v, push='always')
    #     # VALUE
    #     if "value" in cmd_att:
    #         v = cmd_att["value"]
    #         if not isinstance(v, int) and not isinstance(v, str):
    #             raise Exception(f"Invalid type for direction.value {type(v)}")
    #         try:
    #             self._PZADRV_DIO_set_direction_value(v)
    #             self._update_attributes_from_dict(
    #                 {
    #                     "direction": {
    #                         "value": self._PZADRV_DIO_get_direction_value()
    #                     }
    #                 })
    #         except Exception as e:
    #             self.log.error(f"{e}")

    #     if "pull" in cmd_att:
    #         v = cmd_att["pull"]
    #         if not isinstance(v, int) and not isinstance(v, str):
    #             raise Exception(f"Invalid type for direction.pull {type(v)}")
    #         try:
    #             self._PZADRV_DIO_set_direction_pull(v)
    #             self._update_attributes_from_dict(
    #                 {
    #                     "direction": {
    #                         "pull": self._PZADRV_DIO_get_direction_pull()
    #                     }
    #                 })
    #         except Exception as e:
    #             self.log.error(f"{e}")


    # # update the state attribut field
    # def __handle_cmd_set_state_dio(elf, cmd_att):
    #     if "polling_cycle" in cmd_att:
    #         v = cmd_att["polling_cycle"]
    #         if not isinstance(v, int) and not isinstance(v, float):
    #             raise Exception(f"Invalid type for volts.polling_cycle {type(v)}")
    #         if v < 0:
    #             v = -1
    #         elf._update_attribute("state", "polling_cycle", v, push='always')
    #     # VALUE
    #     if "active" in cmd_att:
    #         v = cmd_att["active"]
    #         elf.log.debug("test active state")
    #         if not isinstance(v, int) and not isinstance(v, str):
    #             raise Exception(f"Invalid type for state.active {type(v)}")
    #         try:
    #             elf._PZADRV_DIO_set_state_active(v)
    #             elf._update_attributes_from_dict(
    #                 {
    #                     "state": {
    #                         "active": elf._PZADRV_DIO_get_state_active()
    #                     }
    #                 })
    #         except Exception as e:
    #             elf.log.error(f"{e}")

    #     if "active_low" in cmd_att:
    #         v = cmd_att["active_low"]
    #         if not isinstance(v, int) and not isinstance(v, str):
    #             raise Exception(f"Invalid type for state.active low {type(v)}")
    #         try:
    #             elf._PZADRV_DIO_set_state_activeLow(v)
    #             elf._update_attributes_from_dict(
    #                 {
    #                     "state": {
    #                         "active_low": elf._PZADRV_DIO_get_state_activeLow()
    #                     }
    #                 })
    #         except Exception as e:
    #             elf.log.error(f"{e}")
                

