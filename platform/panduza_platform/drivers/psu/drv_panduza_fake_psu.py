import time
from collections import ChainMap
from ...meta_drivers.psu import MetaDriverPsu

class DrvPanduzaFakePsu(MetaDriverPsu):
    """Fake PSU driver
    """

    # =============================================================================
    # FROM MetaDriverPsu

    # ---

    def _PZA_DRV_PSU_config(self):
        """
        """
        return {
            "name": "panduza.fake.psu",
            "description": "Virtual PSU"
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

        # Call meta class PSU ini
        await super()._PZA_DRV_loop_init(loop, tree)

    ###########################################################################

    def _PZA_DRV_PSU_read_enable_value(self):
        # self.log.debug(f"read enable !")
        return self.__fakes["enable"]["value"]

    # ---

    def _PZA_DRV_PSU_write_enable_value(self, v):
        self.log.info(f"write enable : {v}")
        self.__fakes["enable"]["value"] = v

    ###########################################################################

    def _PZA_DRV_PSU_read_volts_goal(self):
        # self.log.debug(f"read volts goal !")
        return self.__fakes["volts"]["goal"]

    # ---

    def _PZA_DRV_PSU_write_volts_goal(self, v):
        self.log.info(f"write volts : {v}")
        self.__fakes["volts"]["goal"] = v
        self.__fakes["volts"]["real"] = v
    
    # ---

    def _PZA_DRV_PSU_volts_goal_min_max(self):
        return {
            "min": self.__fakes["volts"]["min"],
            "max": self.__fakes["volts"]["max"] 
        }

    # ---

    def _PZA_DRV_PSU_read_volts_real(self):
        # self.log.debug(f"read volts real !")
        return self.__fakes["volts"]["real"]

    # ---

    def _PZA_DRV_PSU_read_volts_decimals(self):
        return self.__fakes["volts"]["decimals"]

    ###########################################################################

    def _PZA_DRV_PSU_read_amps_goal(self):
        # self.log.debug(f"read amps goal !")
        return self.__fakes["amps"]["goal"]

    # ---

    def _PZA_DRV_PSU_write_amps_goal(self, v):
        self.log.info(f"write amps : {v}")
        self.__fakes["amps"]["goal"] = v
        self.__fakes["amps"]["real"] = v

    # ---

    def _PZA_DRV_PSU_amps_goal_min_max(self):
        return {
            "min": self.__fakes["amps"]["min"],
            "max": self.__fakes["amps"]["max"] 
        }

    # ---

    def _PZA_DRV_PSU_read_amps_real(self):
        # self.log.debug(f"read amps real !")
        return self.__fakes["amps"]["real"]

    # ---

    def _PZA_DRV_PSU_read_amps_decimals(self):
        return self.__fakes["amps"]["decimals"]

    ###########################################################################
    ###########################################################################

    def _PZA_DRV_PSU_settings_capabilities(self):
        return self.__fakes["settings_capabilities"]

    # ---

    def _PZA_DRV_PSU_read_settings_ovp(self):
        return self.__fakes["settings"]["ovp"]

    def _PZA_DRV_PSU_write_settings_ovp(self, v):
        self.__fakes["settings"]["ovp"] = v

    # ---

    def _PZA_DRV_PSU_read_settings_ocp(self):
        return self.__fakes["settings"]["ocp"]

    def _PZA_DRV_PSU_write_settings_ocp(self, v):
        self.__fakes["settings"]["ocp"] = v

    # ---

    def _PZA_DRV_PSU_read_settings_silent(self):
        return self.__fakes["settings"]["silent"]

    def _PZA_DRV_PSU_write_settings_silent(self, v):
        self.__fakes["settings"]["silent"] = v

    ###########################################################################
    ###########################################################################

    def _PZA_DRV_PSU_read_misc(self):
        return self.__fakes["misc"]

    # ---

    def _PZA_DRV_PSU_write_misc(self, field, v):
        pass
