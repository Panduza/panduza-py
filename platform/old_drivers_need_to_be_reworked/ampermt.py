import time
from ..meta_driver import MetaDriver

class MetaDriverAmpermt(MetaDriver):
    """
    """

    ###########################################################################
    ###########################################################################
    #
    # TO OVERRIDE IN DRIVER
    #
    ###########################################################################
    ###########################################################################

    def _PZA_DRV_AMPERMT_read_value(self):
        """
        """
        raise NotImplementedError("Must be implemented !")

    ###########################################################################
    ###########################################################################
    #
    # MATA DRIVER OVERRIDE
    #
    ###########################################################################
    ###########################################################################

    def _PZA_DRV_config(self):
        """Driver base configuration
        """
        return {
            "info": {
                "type": "ampermt",
                "version": "0.0"
            },
        }

    # ---

    def _PZA_DRV_loop_init(self, loop, tree):
        # Set command handlers
        self.__cmd_handlers = {
            "measure": self.__handle_cmds_set_measure,
        }

        # First update
        self.__update_attribute_initial()

        # Polling cycle reset
        start_time = time.perf_counter()
        self.polling_ref = {
            "measure": start_time,
        }

        # Init success, the driver can pass into the run mode
        self._PZA_DRV_init_success()

    # ---

    def _PZA_DRV_loop_run(self, loop):

        self.__poll_att_measure()
        # Limit on python platform
        time.sleep(0.1)

    # ---

    def _PZA_DRV_cmds_set(self, loop, payload):
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

    # ---

    def __poll_att_measure(self):
        polling_cycle = float(self._get_field("measure", "polling_cycle"))
        if polling_cycle < 0:
            return
        if (time.perf_counter() - self.polling_ref["measure"]) > polling_cycle:
            p = False
            p = self._update_attribute("measure", "value", self._PZA_DRV_AMPERMT_read_value(), False) or p
            if p:
                self._push_attribute("measure")
            self.polling_ref["measure"] = time.perf_counter()

    # ---

    def __update_attribute_initial(self):
        p = False
        p = self._update_attribute("measure", "value", self._PZA_DRV_AMPERMT_read_value(), False) or p
        if p:
            self._push_attribute("measure")

    # ---

    def __handle_cmds_set_measure(self, cmd_att):
        """Manage output enable commands
        """
        # POLLING_CYCLE
        if "polling_cycle" in cmd_att:
            v = cmd_att["polling_cycle"]
            if not isinstance(v, int) and not isinstance(v, float):
                raise Exception(f"Invalid type for amps.polling_cycle {type(v)}")
            if v < 0:
                v = -1
            self._update_attribute("measure", "polling_cycle", v, push='always')

