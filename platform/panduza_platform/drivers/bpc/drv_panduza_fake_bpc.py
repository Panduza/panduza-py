import time
from collections import ChainMap
from meta_drivers.bpc import MetaDriverBpc

class DrvPanduzaFakeBpc(MetaDriverBpc):
    """Fake BPC driver
    """

    # =============================================================================
    # FROM MetaDriverBpc

    # ---

    def _PZA_DRV_BPC_config(self):
        """
        """
        return {
            "name": "panduza.fake.bpc",
            "description": "Virtual BPC"
        }

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """Init function
        Reset fake parameters
        """
        self.__fakes = {
            "enable": {
                "value": False
            },
            "volts": {
                "goal": 0,
                "real": 0,
                "min": -1000,
                "max":  1000,
                "decimals": 2
            },
            "amps": {
                "goal":  0,
                "real":  0,
                "min":   0,
                "max":  50,
                "decimals": 3
            },
            "settings_capabilities": {
                "ovp": False,       # Over Voltage Protection
                "ocp": False,       # Over Current Protection
                "silent": False,    # Silent mode
            },
            "settings": {
                "ovp": False,
                "ocp": False,
                "silent": False,
            },
            "misc": {
                "model": "GOUBY42 (Panduza Fake Power Supply)"
            }
        }

        # Call meta class BPC ini
        await super()._PZA_DRV_loop_init(loop, tree)

    ###########################################################################

    async def _PZA_DRV_BPC_read_enable_value(self):
        # self.log.debug(f"read enable !")
        return self.__fakes["enable"]["value"]

    # ---

    async def _PZA_DRV_BPC_write_enable_value(self, v):
        self.log.info(f"write enable : {v}")
        self.__fakes["enable"]["value"] = v

    ###########################################################################

    async def _PZA_DRV_BPC_read_volts_goal(self):
        # self.log.debug(f"read volts goal !")
        return self.__fakes["volts"]["goal"]

    # ---

    async def _PZA_DRV_BPC_write_volts_goal(self, v):
        self.log.info(f"write volts : {v}")
        self.__fakes["volts"]["goal"] = v
        self.__fakes["volts"]["real"] = v
    
    # ---

    async def _PZA_DRV_BPC_volts_goal_min_max(self):
        return {
            "min": self.__fakes["volts"]["min"],
            "max": self.__fakes["volts"]["max"] 
        }

    # ---

    async def _PZA_DRV_BPC_read_volts_decimals(self):
        return self.__fakes["volts"]["decimals"]

    ###########################################################################

    async def _PZA_DRV_BPC_read_amps_goal(self):
        # self.log.debug(f"read amps goal !")
        return self.__fakes["amps"]["goal"]

    # ---

    async def _PZA_DRV_BPC_write_amps_goal(self, v):
        self.log.info(f"write amps : {v}")
        self.__fakes["amps"]["goal"] = v
        self.__fakes["amps"]["real"] = v

    # ---

    async def _PZA_DRV_BPC_amps_goal_min_max(self):
        return {
            "min": self.__fakes["amps"]["min"],
            "max": self.__fakes["amps"]["max"] 
        }

    # ---

    async def _PZA_DRV_BPC_read_amps_decimals(self):
        return self.__fakes["amps"]["decimals"]

