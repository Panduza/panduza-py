import abc
import time
import asyncio
from collections import ChainMap
from ..platform_driver import PlatformDriver

class MetaDriverPsu(PlatformDriver):
    """ Abstract Driver with helper class to manage power supply interface
    """

    # =============================================================================
    # PLATFORM DRIVERS FUNCTIONS

    def _PZA_DRV_config(self):
        """Driver base configuration
        """
        base = {
            "info": {
                "type": "psu",
                "version": "0.0"
            }
        }
        return ChainMap(base, self._PZA_DRV_PSU_config())

    # =============================================================================
    # TO OVERRIDE IN DRIVER

    # ---

    @abc.abstractmethod
    def _PZA_DRV_PSU_config(self):
        """Driver base configuration
        """
        pass

    # ---

    async def _PZA_DRV_PSU_read_enable_value(self):
        """Must get the state value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    async def _PZA_DRV_PSU_write_enable_value(self, v):
        """Must set *v* as the new state value on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    async def _PZA_DRV_PSU_read_volts_goal(self):
        """Must get the volts goal value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    async def _PZA_DRV_PSU_write_volts_goal(self, v):
        """Must set *v* as the new volts goal value on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    async def _PZA_DRV_PSU_volts_goal_min_max(self):
        """Must return the voltage goal range of the power supply
        """
        return {"min": 0, "max": 0 }

    async def _PZA_DRV_PSU_read_volts_decimals(self):
        """Must return the number of decimals supported for the voltage
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    async def _PZA_DRV_PSU_read_amps_goal(self):
        """Must get the amps goal value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    async def _PZA_DRV_PSU_write_amps_goal(self, v):
        """Must set *v* as the new amps goal value on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    async def _PZA_DRV_PSU_amps_goal_min_max(self):
        """Must return the amps range of the power supply
        """
        return {"min": 0, "max": 0 }

    async def _PZA_DRV_PSU_read_amps_decimals(self):
        """Must return the number of decimals supported for the amperage
        """
        raise NotImplementedError("Must be implemented !")

    ###########################################################################
    ###########################################################################
    #
    # FOR SUBCLASS USE ONLY
    #
    ###########################################################################
    ###########################################################################

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        # Set command handlers
        self.__cmd_handlers = {
            "enable": self.__handle_cmds_set_enable,
            "volts": self.__handle_cmds_set_volts,
            "amps": self.__handle_cmds_set_amps,
            # "settings": self.__handle_cmds_set_settings,
        }

        # First update
        await self.__update_attribute_initial()

        # Polling cycle reset
        start_time = time.perf_counter()
        self.polling_ref = {
            "enable": start_time,
            "volts" : start_time,
            "amps"  : start_time,
        }
        
        # Start polling task
        self.__task_polling_att_enable = loop.create_task(self.__polling_task_att_enable())
        self.__task_polling_att_volts = loop.create_task(self.__polling_task_att_volts())
        self.__task_polling_att_amps = loop.create_task(self.__polling_task_att_amps())

        # Init success, the driver can pass into the run mode
        self._PZA_DRV_init_success()

    # ---

    async def _PZA_DRV_cmds_set(self, loop, payload):
        """From MetaDriver
        """
        cmds = self.payload_to_dict(payload)
        # self.log.debug(f"cmds as json : {cmds}")
        for att in self.__cmd_handlers:
            if att in cmds:
                await self.__cmd_handlers[att](cmds[att])

    # =============================================================================
    # PRIVATE FUNCTIONS

   # ---

    def __set_poll_cycle_enable(self, v):
        self.polling_ref["enable"] = v
    def __get_poll_cycle_enable(self):
        return self.polling_ref["enable"]

    # --
    
    def __set_poll_cycle_volts(self, v):
        self.polling_ref["volts"] = v
    def __get_poll_cycle_volts(self):
        return self.polling_ref["volts"]
    
    # --
    
    def __set_poll_cycle_amps(self, v):
        self.polling_ref["amps"] = v
    def __get_poll_cycle_amps(self):
        return self.polling_ref["amps"]
    
    # ---

    async def __polling_task_att_enable(self):
        """Task to poll the value
        """
        while self.alive:
            await asyncio.sleep(self.polling_ref["enable"])
            await self._update_attributes_from_dict({
                "enable": {
                    "value": await self._PZA_DRV_PSU_read_enable_value()
                }
            })

    # ---

    async def __polling_task_att_volts(self):
        """Task to poll the value
        """
        while self.alive:
            await asyncio.sleep(self.polling_ref["volts"])
            await self._update_attributes_from_dict({
                "volts": {
                    "goal": await self._PZA_DRV_PSU_read_volts_goal()
                }
            })

    # ---

    async def __polling_task_att_amps(self):
        """Task to poll the value
        """
        while self.alive:
            await asyncio.sleep(self.polling_ref["amps"])
            await self._update_attributes_from_dict({
                "amps": {
                    "goal": await self._PZA_DRV_PSU_read_amps_goal()
                }
            })

    # ---

    async def __update_attribute_initial(self):
        """
        """
        await self.__att_enable_full_update()
        await self.__att_volts_full_update()
        await self.__att_amps_full_update()

    # ---

    async def __handle_cmds_set_enable(self, cmd_att):
        """Manage output enable commands
        """
        update_obj = {}
        await self._prepare_update(update_obj, 
                            "enable", cmd_att,
                            "value", [bool]
                            , self._PZA_DRV_PSU_write_enable_value
                            , self._PZA_DRV_PSU_read_enable_value)
        await self._prepare_update(update_obj, 
                            "enable", cmd_att,
                            "polling_cycle", [float, int]
                            , self.__set_poll_cycle_enable
                            , self.__get_poll_cycle_enable)
        await self._update_attributes_from_dict(update_obj)

    # ---

    async def __handle_cmds_set_volts(self, cmd_att):
        """Manage voltage commands
        """
        update_obj = {}
        
        # TODO
        # if self._get_field("volts", "min") <= v <= self._get_field("volts", "max"):
                
        await self._prepare_update(update_obj, 
                            "volts", cmd_att,
                            "goal", [float, int]
                            , self._PZA_DRV_PSU_write_volts_goal
                            , self._PZA_DRV_PSU_read_volts_goal)
        
        await self._prepare_update(update_obj, 
                            "volts", cmd_att,
                            "polling_cycle", [float, int]
                            , self.__set_poll_cycle_volts
                            , self.__get_poll_cycle_volts)
        
        await self._update_attributes_from_dict(update_obj)

    # ---

    async def __handle_cmds_set_amps(self, cmd_att):
        """Manage ampere commands
        """
        update_obj = {}
        
        # TODO
        # if self._get_field("amps", "min") <= v <= self._get_field("amps", "max"):
                
        await self._prepare_update(update_obj, 
                            "amps", cmd_att,
                            "goal", [float, int]
                            , self._PZA_DRV_PSU_write_amps_goal
                            , self._PZA_DRV_PSU_read_amps_goal)
        
        await self._prepare_update(update_obj, 
                            "amps", cmd_att,
                            "polling_cycle", [float, int]
                            , self.__set_poll_cycle_amps
                            , self.__get_poll_cycle_amps)
        
        await self._update_attributes_from_dict(update_obj)

    # ---

    async def __att_enable_full_update(self):
        """
        """
        await self._update_attributes_from_dict({
            "enable": {
                "value": await self._PZA_DRV_PSU_read_enable_value(),
                "polling_cycle": 1
            }
        })

    # ---

    async def __att_volts_full_update(self):
        """
        """
        min_max = await self._PZA_DRV_PSU_volts_goal_min_max()
        await self._update_attributes_from_dict({
            "volts": {
                "min": min_max.get("min", 0),
                "max": min_max.get("max", 0),
                "goal": await self._PZA_DRV_PSU_read_volts_goal(),
                "decimals": await self._PZA_DRV_PSU_read_volts_decimals(),
                "polling_cycle": 1
            }
        })

    # ---

    async def __att_amps_full_update(self):
        """
        """
        min_max = await self._PZA_DRV_PSU_amps_goal_min_max()
        await self._update_attributes_from_dict({
            "amps": {
                "min": min_max.get("min", 0),
                "max": min_max.get("max", 0),
                "goal": await self._PZA_DRV_PSU_read_amps_goal(),
                "decimals": await self._PZA_DRV_PSU_read_amps_decimals(),
                "polling_cycle": 1
            }
        })

