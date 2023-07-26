import io
from collections import ChainMap
from meta_drivers.bps import MetaDriverBps
from connectors.serial_tty import ConnectorSerialTty

from connectors.udev_tty import HuntUsbDevs

QL355P_USBID_VENDOR="103e"
QL355P_USBID_MODEL="03e8"
QL355P_SERIAL_BAUDRATE=19200
QL355P_TTY_BASE="/dev/ttyUSB"

STATE_VALUE_ENUM = { True: 1, False: 0 }
VOLTS_BOUNDS     = { "min": 0, "max": 30 }
AMPS_BOUNDS      = { "min": 0, "max":  5 }


class DriverQL355P(MetaDriverBps):
    """Driver for the device QL355P from aim-TTI
    """
    
    ###########################################################################
    ###########################################################################

    def _PZA_DRV_config(self):
        # Extend the common bps config
        return ChainMap(super()._PZA_DRV_config(), {
            "name": "Py_Bps_QL355P",
            "description": "Power Supply QL355P",
            "compatible": [
                "ql355p",
                "aimtty.ql355p",
                "bps.aimtty.ql355p",
                "py.bps.aimtty.ql355p"
            ]
        })

    def __tgen(serial_short, name_suffix):
        return {
            "name": "QL355P:" + name_suffix,
            "driver": "py.bps.aimtty.ql355p",
            "settings": {
                "serial_short": serial_short
            }
        }

    def _PZA_DRV_tree_template(self):
        return DriverQL355P.__tgen("USB: Short Serial ID", "template")

    def _PZA_DRV_hunt_instances(self):
        instances = []
        usb_pieces = HuntUsbDevs(vendor=QL355P_USBID_VENDOR, model=QL355P_USBID_MODEL, subsystem="tty")
        for p in usb_pieces:
            iss = p["ID_SERIAL_SHORT"]
            instances.append(DriverQL355P.__tgen(iss, iss))
        return instances

    ###########################################################################
    ###########################################################################

    def _PZA_DRV_loop_init(self, loop, tree):

        # Get settings from tree and append constant settings for this device
        settings = dict() if "settings" not in tree else tree["settings"]
        settings["vendor"] = QL355P_USBID_VENDOR
        settings["model"] = QL355P_USBID_MODEL
        settings["baudrate"] = QL355P_SERIAL_BAUDRATE
        settings["base_devname"] = QL355P_TTY_BASE
        
        # Get the connector
        self.serp = ConnectorSerialTty.Get(**settings)

        # TODO : Bad pratice "get_internal_driver" but used to speed up
        # https://stackoverflow.com/questions/10222788/line-buffered-serial-input
        self.io  = io.TextIOWrapper(
            self.serp.get_internal_driver(),
            encoding       = "ascii",
            newline        = None,
            line_buffering = False
        )
        self.io._CHUNK_SIZE= 1
        

        # TODO :Bad pratice with loopback variable instead of reading the value back
        self.state = "off"
        self.volts = 0
        self.amps = 0

        # Constants Fields settings
        self._PZA_DRV_BPS_update_volts_min_max(VOLTS_BOUNDS["min"], VOLTS_BOUNDS["max"])
        self._PZA_DRV_BPS_update_amps_min_max(AMPS_BOUNDS["min"], AMPS_BOUNDS["max"])

        # Misc
        self._PZA_DRV_BPS_update_misc("model", "QL355P (AIM-TTI)")

        # Call meta class BPS ini
        super()._PZA_DRV_loop_init(tree)


    ###########################################################################
    ###########################################################################

    def __write(self, *cmds):
        # Append new line terminator to all commands
        txt = "".join( map(lambda x: f"{x}\r\n", cmds) )

        self.log.debug(f"TX: {txt!r}")
        self.io.write(txt)
        self.io.flush()

    ###########################################################################
    ###########################################################################

    # STATE #

    def _PZA_DRV_BPS_read_enable_value(self):
        return self.state

    # ---

    def _PZA_DRV_BPS_write_enable_value(self, v):
        self.state = v
        cmd = STATE_VALUE_ENUM[v]
        self.__write(f"OP1 {int(cmd)}")

    # VOLTS #

    def _PZA_DRV_BPS_read_volts_goal(self):
        return self.volts

    # ---

    def _PZA_DRV_BPS_read_volts_real(self):
        return 0
    
    # ---

    def _PZA_DRV_BPS_write_volts_goal(self, v):
        self.volts = v
        self.__write(f"V1 {v:.3f}")

    # ---

    def _PZA_DRV_BPS_volts_goal_min_max(self):
        return VOLTS_BOUNDS
    # ---

    def _PZA_DRV_BPS_read_volts_decimals(self):
        return 2

    # AMPS #
    
    def _PZA_DRV_BPS_read_amps_goal(self):
        return self.amps

    # ---

    def _PZA_DRV_BPS_write_amps_goal(self, v):
        self.amps = v
        self.__write(f"I1 {v:.3f}")

    # ---
    
    def _PZA_DRV_BPS_amps_goal_min_max(self):
        return AMPS_BOUNDS
    
    # ---

    def _PZA_DRV_BPS_read_amps_real(self):
        return 0

    # ---

    def _PZA_DRV_BPS_read_amps_decimals(self):
        return 3
    
    # SETTINGS #

    def _PZA_DRV_BPS_settings_capabilities(self):
        return  {
            "ovp": False,
            "ocp": False,
            "silent": False,
        }
    
    ###########################################################################
    ###########################################################################

    def PZADRV_hunt():
        """
        """
        return None

