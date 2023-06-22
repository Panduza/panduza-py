import json
import base64
from ..meta_driver import MetaDriver

class MetaDriverSerial(MetaDriver):
    """ Abstract Driver with helper class to manage power supply interface
    """
    
    ###########################################################################
    ###########################################################################
    #
    # MATA DRIVER OVERRIDE
    #
    ###########################################################################
    ###########################################################################

    def _PZA_DRV_config(self):
        return {
            "info": {
                "type": "serial",
                "version": "1.0"
            },
        }

    def _PZA_DRV_loop_init(self, loop, tree):

        self.__cmd_handlers = {
            "data": self.__handle_cmds_set_data
        }

        # default = dict() if "default" not in tree else tree["default"]
        # self._update_attributes_from_dict(default)

        self._PZA_DRV_init_success()

    def _PZA_DRV_loop_run(self, loop):
        pass

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
    # FOR SUBCLASS USE ONLY
    #
    ###########################################################################
    ###########################################################################


    def _PZA_DRV_SERIAL_data_received(self, rx_data: bytes):
        """
        """
        # *bytes* to *base64 bytes*
        rx_base64_bytes = base64.b64encode(rx_data)
        # *base64 bytes* to *base64 string*
        rx_base64_string = rx_base64_bytes.decode('ascii')
        # 
        self._update_attribute("data", "rx", rx_base64_string)


    ###########################################################################
    ###########################################################################
    #
    # TO OVERRIDE IN DRIVER
    #
    ###########################################################################
    ###########################################################################



    def _PZA_DRV_SERIAL_write_data(self, v):
        """
        """
        raise NotImplementedError("Must be implemented !")

    ###########################################################################
    ###########################################################################
    #
    # PRIVATE
    #
    ###########################################################################
    ###########################################################################

    def __handle_cmds_set_data(self, cmd_att):
        """
        """
        if "tx" in cmd_att:
            v = cmd_att["tx"]
            base64_bytes = v.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            try:
                self._PZA_DRV_SERIAL_write_data(message_bytes)
            except Exception as e:
                self.log.error(f"{e}")

