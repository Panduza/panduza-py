import time
from ..meta_driver import MetaDriver

class MetaDriverPsu(MetaDriver):
    """ Abstract Driver with helper class to manage power supply interface
    """

    ###########################################################################
    ###########################################################################
    #
    # TO OVERRIDE IN DRIVER
    #
    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_enable_value(self):
        """Must get the state value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_enable_value(self, v):
        """Must set *v* as the new state value on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    def _PZADRV_PSU_read_volts_goal(self):
        """Must get the volts goal value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_volts_goal(self, v):
        """Must set *v* as the new volts goal value on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_volts_goal_min_max(self):
        """Must return the voltage goal range of the power supply
        """
        return {"min": 0, "max": 0 }

    def _PZADRV_PSU_read_volts_real(self):
        """Must get the volts real value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_read_volts_decimals(self):
        """Must return the number of decimals supported for the voltage
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    def _PZADRV_PSU_read_amps_goal(self):
        """Must get the amps goal value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_amps_goal(self, v):
        """Must set *v* as the new amps goal value on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_amps_goal_min_max(self):
        """Must return the amps range of the power supply
        """
        return {"min": 0, "max": 0 }

    def _PZADRV_PSU_read_amps_real(self):
        """Must get the amperage real value on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_read_amps_decimals(self):
        """Must return the number of decimals supported for the amperage
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    def _PZADRV_PSU_settings_capabilities(self):
        """Must return settings capabilities
        """
        return {
            "ovp": False,       # Over Voltage Protection
            "ocp": False,       # Over Current Protection
            "silent": False,    # Silent mode
        }

    def _PZADRV_PSU_read_settings_ovp(self):
        """Must get the ovp state on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_settings_ovp(self, v):
        """Must set *v* as the new ovp state on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_read_settings_ocp(self):
        """Must get the ocp state on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_settings_ocp(self, v):
        """Must set *v* as the new ocp state on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_read_settings_silent(self):
        """Must get the silent state on the PSU and return it
        """
        raise NotImplementedError("Must be implemented !")

    def _PZADRV_PSU_write_settings_silent(self, v):
        """Must set *v* as the new silent state on the PSU
        """
        raise NotImplementedError("Must be implemented !")

    # ---

    def _PZADRV_PSU_read_misc(self):
        """
        """
        return { }

    def _PZADRV_PSU_write_misc(self, field, v):
        """
        """
        pass

    ###########################################################################
    ###########################################################################
    #
    # FOR SUBCLASS USE ONLY
    #
    ###########################################################################
    ###########################################################################

    def _pzadrv_psu_update_volts_min_max(self, min, max):
        self.log.warning(f"!!! DEPRECATED !!! _pzadrv_psu_update_volts_min_max")
        self._update_attribute("volts", "min", min, False)
        self._update_attribute("volts", "max", max)

    # ---

    def _pzadrv_psu_update_amps_min_max(self, min, max):
        self.log.warning(f"!!! DEPRECATED !!! _pzadrv_psu_update_amps_min_max")
        self._update_attribute("amps", "min", min, False)
        self._update_attribute("amps", "max", max)

    # ---

    def _pzadrv_psu_update_misc(self, field, value):
        self.log.warning(f"!!! DEPRECATED !!! _pzadrv_psu_update_misc")
        self._update_attribute("misc", field, value)
        
    ###########################################################################
    ###########################################################################
    #
    # MATA DRIVER OVERRIDE
    #
    ###########################################################################
    ###########################################################################

    def _PZADRV_config(self):
        """Driver base configuration
        """
        return {
            "info": {
                "type": "psu",
                "version": "1.0"
            },
        }

    # ---

    def _PZADRV_loop_init(self, tree):
        # Set command handlers
        self.__cmd_handlers = {
            "enable": self.__handle_cmds_set_enable,
            "volts": self.__handle_cmds_set_volts,
            "amps": self.__handle_cmds_set_amps,
            "settings": self.__handle_cmds_set_settings,
            "misc": self.__handle_cmds_set_misc,
        }

        # First update
        self.__update_attribute_initial()

        # Polling cycle reset
        start_time = time.perf_counter()
        self.polling_ref = {
            "enable": start_time,
            "volts" : start_time,
            "amps"  : start_time,
        }

        # Init success, the driver can pass into the run mode
        self._pzadrv_init_success()

    # ---

    def _PZADRV_loop_run(self):
        # Polls
        self.__poll_att_enable()
        self.__poll_att_volts()
        self.__poll_att_amps()
        # Limit on python platform
        time.sleep(0.1)

    # ---

    def _PZADRV_cmds_set(self, payload):
        """From MetaDriver
        """
        cmds = self.payload_to_dict(payload)
        # self.log.debug(f"cmds as json : {cmds}")
        for att in self.__cmd_handlers:
            if att in cmds:
                self.__cmd_handlers[att](cmds[att])

    ###########################################################################
    ###########################################################################
    #
    # PRIVATE
    #
    ###########################################################################
    ###########################################################################

    def __poll_att_enable(self):
        polling_cycle = float(self._get_field("enable", "polling_cycle"))
        if polling_cycle < 0:
            return
        if (time.perf_counter() - self.polling_ref["enable"]) > polling_cycle:
            self._update_attribute("enable", "value", self._PZADRV_PSU_read_enable_value())
            self.polling_ref["enable"] = time.perf_counter()

    # ---

    def __poll_att_volts(self):
        polling_cycle = float(self._get_field("volts", "polling_cycle"))
        if polling_cycle < 0:
            return
        if (time.perf_counter() - self.polling_ref["volts"]) > polling_cycle:
            p = False
            p = self._update_attribute("volts", "goal", self._PZADRV_PSU_read_volts_goal(), False) or p
            p = self._update_attribute("volts", "real", self._PZADRV_PSU_read_volts_real(), False) or p
            if p:
                self._push_attribute("volts")
            self.polling_ref["volts"] = time.perf_counter()

    # ---

    def __poll_att_amps(self):
        polling_cycle = float(self._get_field("amps", "polling_cycle"))
        if polling_cycle < 0:
            return
        if (time.perf_counter() - self.polling_ref["amps"]) > polling_cycle:
            p = False
            p = self._update_attribute("amps", "goal", self._PZADRV_PSU_read_amps_goal(), False) or p
            p = self._update_attribute("amps", "real", self._PZADRV_PSU_read_amps_real(), False) or p
            if p:
                self._push_attribute("amps")
            self.polling_ref["amps"] = time.perf_counter()

    # ---

    def __update_attribute_initial(self):
        # === ENABLE
        self._update_attribute("enable", "value", self._PZADRV_PSU_read_enable_value())
        self._update_attribute("enable", "polling_cycle", 5)

        # === VOLTS
        p = False
        min_max = self._PZADRV_PSU_volts_goal_min_max()
        # /!\ 'or p' must be at the end
        p = self._update_attribute("volts", "min", min_max.get("min", 0), False) or p
        p = self._update_attribute("volts", "max", min_max.get("max", 0), False) or p
        p = self._update_attribute("volts", "goal", self._PZADRV_PSU_read_volts_goal(), False) or p
        p = self._update_attribute("volts", "real", self._PZADRV_PSU_read_volts_real(), False) or p
        p = self._update_attribute("volts", "decimals", self._PZADRV_PSU_read_volts_decimals(), False) or p
        p = self._update_attribute("volts", "polling_cycle", 5, False) or p
        if p:
            self._push_attribute("volts")

        # === AMPS
        p = False
        min_max = self._PZADRV_PSU_amps_goal_min_max()
        # /!\ 'or p' must be at the end
        p = self._update_attribute("amps", "min", min_max.get("min", 0), False) or p
        p = self._update_attribute("amps", "max", min_max.get("max", 0), False) or p
        p = self._update_attribute("amps", "goal", self._PZADRV_PSU_read_amps_goal(), False) or p
        p = self._update_attribute("amps", "real", self._PZADRV_PSU_read_amps_real(), False) or p
        p = self._update_attribute("amps", "decimals", self._PZADRV_PSU_read_amps_decimals(), False) or p
        p = self._update_attribute("amps", "polling_cycle", 5, False) or p
        if p:
            self._push_attribute("amps")

        # === SETTINGS
        p = False
        # /!\ 'or p' must be at the end
        sc = self._PZADRV_PSU_settings_capabilities()
        if sc.get("ovp", False):
            p = self._update_attribute("settings", "ovp", self._PZADRV_PSU_read_settings_ovp(), False) or p
        if sc.get("ocp", False):
            p = self._update_attribute("settings", "ocp", self._PZADRV_PSU_read_settings_ocp(), False) or p
        if sc.get("silent", False):
            p = self._update_attribute("settings", "silent", self._PZADRV_PSU_read_settings_silent(), False) or p
        if p:
            self._push_attribute("settings")

        # === MISC
        self._update_attributes_from_dict({
            "misc": self._PZADRV_PSU_read_misc()
        })

    # ---
    
    def __handle_cmds_set_enable(self, cmd_att):
        """Manage output enable commands
        """
        if "value" in cmd_att:
            # Control field type
            v = cmd_att["value"]
            if not isinstance(v, bool):
                raise Exception(f"Invalid type for enable.value {type(v)}")
            # Call driver implementations
            try:
                self._PZADRV_PSU_write_enable_value(v)
                self._update_attribute("enable", "value", v)
            except Exception as e:
                raise Exception(f"Fail to set enable.value ({e})")

    # ---

    def __handle_cmds_set_volts(self, cmd_att):
        """Manage voltage commands
        """
        # POLLING_CYCLE
        if "polling_cycle" in cmd_att:
            v = cmd_att["polling_cycle"]
            if not isinstance(v, int) and not isinstance(v, float):
                raise Exception(f"Invalid type for volts.polling_cycle {type(v)}")
            if v < 0:
                v = -1
            self._update_attribute("volts", "polling_cycle", v)
            
        # GOAL
        if "goal" in cmd_att:
            v = cmd_att["goal"]
            if not isinstance(v, int) and not isinstance(v, float):
                raise Exception(f"Invalid type for volts.goal {type(v)}")
            try:
                if self._get_field("volts", "min") <= v <= self._get_field("volts", "max"):
                    self._PZADRV_PSU_write_volts_goal(v)
                    self._update_attributes_from_dict(
                    {
                        "volts": {
                            "goal": self._PZADRV_PSU_read_volts_goal(),
                            "real": self._PZADRV_PSU_read_volts_real()
                        }
                    })
                else:
                    self.log.error(
                        f"goal {v} out of range {self._get_field('volts', 'min')} < {self._get_field('volts', 'max')}")

            except Exception as e:
                self.log.error(f"{e}")

    # ---

    def __handle_cmds_set_amps(self, cmd_att):
        """Manage ampere commands
        """
        # POLLING_CYCLE
        if "polling_cycle" in cmd_att:
            v = cmd_att["polling_cycle"]
            if not isinstance(v, int) and not isinstance(v, float):
                raise Exception(f"Invalid type for amps.polling_cycle {type(v)}")
            if v < 0:
                v = -1
            self._update_attribute("amps", "polling_cycle", v)
            
        # GOAL
        if "goal" in cmd_att:
            v = cmd_att["goal"]
            if not isinstance(v, int) and not isinstance(v, float):
                raise Exception(f"Invalid type for amps.goal {type(v)}")
            try:
                if self._get_field("amps", "min") <= v <= self._get_field("amps", "max"):
                    self._PZADRV_PSU_write_amps_goal(v)
                    self._update_attributes_from_dict(
                    {
                        "amps": {
                            "goal": self._PZADRV_PSU_read_amps_goal(),
                            "real": self._PZADRV_PSU_read_amps_real()
                        }
                    })
                else:
                    self.log.error(
                        f"goal {v} out of range {self._get_field('amps', 'min')} < {self._get_field('amps', 'max')}")
            except Exception as e:
                self.log.error(f"{e}")

    # ---

    def __handle_cmds_set_settings(self, cmd_att):
        if "ovp" in cmd_att:
            v = cmd_att["ovp"]
            self._PZADRV_PSU_write_settings_ovp(v)
            self._update_attribute("settings", "ovp", self._PZADRV_PSU_read_settings_ovp())
        if "ocp" in cmd_att:
            v = cmd_att["ocp"]
            self._PZADRV_PSU_write_settings_ocp(v)
            self._update_attribute("settings", "ocp", self._PZADRV_PSU_read_settings_ocp())
        if "silent" in cmd_att:
            v = cmd_att["silent"]
            self._PZADRV_PSU_write_settings_silent(v)
            self._update_attribute("settings", "silent", self._PZADRV_PSU_read_settings_silent())

    # ---

    def __handle_cmds_set_misc(self, cmd_att):
        pass

