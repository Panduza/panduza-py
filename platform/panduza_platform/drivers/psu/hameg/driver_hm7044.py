import io
import time
import re
import traceback

from threading import RLock

from loguru import logger


from collections import ChainMap
from dataclasses import dataclass

from panduza_platform.meta_drivers.psu      import MetaDriverPsu
from panduza_platform.connectors.serial_tty import ConnectorSerialTty

from functools import reduce

from panduza_platform.connectors.udev_tty   import HuntUsbDevs

from threading                              import Event

STATE_VALUE_ENUM       = {"on": True, "off": False}
VOLTS_BOUNDS           = {"min": 0, "max": 30}
AMPS_BOUNDS            = {"min": 0, "max": 1 }

HM7044_SERIAL_BAUDRATE = 9600
HM7044_SERIAL_BYTESIZE = 8
HM7044_SERIAL_STOPBITS = 2
HM7044_SERIAL_PARITY   = "N"

HM7044_THROTTLE_DELAY  = 0.025 # I want to die...

HM7044_TTY_BASE        = "/dev/ttyUSB"

@dataclass
class HM7044ChannelProps:
    volts: float = 0.0
    amps:  float = 0.0
    on:    bool  = False


class ConnectorHM7044:
    """
    Connector object that attaches to the transport connector
    of the target HM7044 devices to handle global properties, etc.
    """

    __instances      = {}
    __instances_lock = RLock()

    ###########################################################################
    ###########################################################################

    @staticmethod
    def Get(**kwargs):
        instance = None
        with ConnectorHM7044.__instances_lock:
            logger.debug(f"Get from {ConnectorHM7044.__instances}")
            instance = ConnectorHM7044.__instances.get(id(kwargs["connector"]), None)
            logger.debug(instance)

            if instance is None:
                try:
                    logger.debug(">> Creating instance")
                    instance = ConnectorHM7044(kwargs["connector"])
                    logger.debug(f"Created instance")
                    ConnectorHM7044.__instances.update({id(kwargs["connector"]): instance})
                    logger.debug(f"Instances: {ConnectorHM7044.__instances}")

                except Exception as exc:
                    logger.error(traceback.format_exc())

        return instance


    ###########################################################################
    ###########################################################################

    def __init__(self, conn):
        self.__conn     = conn
        self.__channels = [HM7044ChannelProps(),HM7044ChannelProps(),HM7044ChannelProps(),HM7044ChannelProps()]

        self.__lock     = RLock()

        self.__io = io.TextIOWrapper(
            self.__conn.get_internal_driver(),
            encoding        = "ascii",
            newline         = "\r",
            line_buffering  = False
        )
        self.__io._CHUNK_SIZE = 1


        #self.reset()
        self.state_sync()

    def __req(self, *cmds):
        resps = []
        with self.__lock:
            # Append new line terminator to all commands

            for cmd in cmds:
                logger.info(f"TX: {cmd}\\r")

                self.__io.write(f"{cmd}\r")
                self.__io.flush()
                time.sleep(HM7044_THROTTLE_DELAY) # Please kill me...

                resps.append(self.__read().strip())
                logger.info(f"RX: {resps[-1]}")

        return resps

    def __read(self):
        buf = self.__io.readline()
        return buf

    ###########################################################################
    ###########################################################################

    def state_sync(self):
        buf = self.__req("READ")[0]

        # Quick and dirty stuff parsing
        fields    = [x.strip() for x in buf.split(";")]
        SPACE_REG = re.compile(r"\s+")

        voltages  = [x.strip() for x in SPACE_REG.sub(" ", fields[0]).split(" ")]
        currents  = [x.strip() for x in SPACE_REG.sub(" ", fields[1]).split(" ")]
        flags     = [x.strip() for x in SPACE_REG.sub(" ", fields[2]).split(" ")]

        logger.debug(voltages)
        logger.debug(currents)
        logger.debug(flags)

        for i in range(4):
            self.__channels[i].volts = float(voltages[i].replace("V", "").strip())
            self.__channels[i].amps  = float(currents[i].replace("A", "").strip())
            self.__channels[i].on    = not(flags[i*2].startswith("OFF"))


    ###########################################################################
    ###########################################################################

    def channel_validate(self, chan: int):
        if (chan < 0) or (chan >= 4):
            raise ValueError(f"{chan} is not between [0-3]")

    def state(self, chan: int) -> bool:
        self.channel_validate(chan)
        return self.__channels[chan].on

    def reset(self):
        cmds = ["SEL ALL", "OFF", "DIS", "SEL N"]
        self.__req(*cmds)

    def enable(self, chan: int, state: bool):
        self.channel_validate(chan)

        # Send select and ON command
        cmds = [f"SEL {chan+1}", "ON" if state else "OFF"]

        if state:
            # Check wether we will need to enable output or not
            will_enable = not(reduce(lambda a,b: a and b, [x.on for x in self.__channels], False))
            if will_enable:
                cmds.append("EN")
        else:
            # Check wether we will need to disable output or not
            will_disable = reduce(lambda a,b: a + (b==True), [x.on for x in self.__channels], 0) == 1

            if will_disable:
                cmds.append("DIS")

        cmds.append("SEL N")

        # Send commands
        self.__req(*cmds)

        # Update local status
        self.__channels[chan].on = state


    def volts_get(self, chan: int):
        logger.debug(f"Get voltage from channel {chan}")
        logger.debug(self.__channels)
        self.channel_validate(chan)
        return self.__channels[chan].volts

    def volts_set(self, chan: int, volts: float):
        self.channel_validate(chan)

        # Send select and SET command
        cmds = [f"SEL {chan+1}", f"SET {volts}V", "SEL N"]

        # Send commands
        self.__req(*cmds)

        # Update local status
        self.__channels[chan].volts = volts


    def amps_set(self, chan: int, amps: float):
        self.channel_validate(chan)

        # Select and SET command
        cmds = [f"SEL {chan+1}", f"SET {amps}A", "SEL N"]

        # Send commands
        self.__req(*cmds)

        # Update local status
        self.__channels[chan].amps = amps


    def amps_get(self, chan: int):
        self.channel_validate(chan)
        return self.__channel[chan].amps


class DriverHM7044(MetaDriverPsu):
    instances = {}

    def _PZADRV_config(self):
        return ChainMap(super()._PZADRV_config(), {
            "name":        "Py_Psu_HM7044",
            "description": "Power Supply HM7044",
            "compatible": [
                "hm7044",
                "hameg.hm7044",
                "psu.hameg.hm7044",
                "py.psu.hameg.hm7044"
            ]
        })

    def _PZADRV_tree_template(self):
        return {
            "name": "HM7044:template",
            "driver": "py.psu.hameg.hm7044",
            "settings": {
                "serial_short": "USBSERIAL",
                "channel": 0,
            }
        }

    def _PZADRV_hunt_instances(self):
        pass

    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_ini(self, tree):
        settings                 = tree.get("settings", dict())

        settings["baudrate"]     = HM7044_SERIAL_BAUDRATE
        settings["base_devname"] = HM7044_TTY_BASE
        settings["bytesize"]     = 8
        settings["stopbits"]     = 2
        settings["parity"  ]     = "N"
        settings["rtscts"  ]     = False

        self.serp    = ConnectorSerialTty.Get(**settings)
        self.handle  = ConnectorHM7044.Get(connector=self.serp)

        self.channel = settings["channel"]

        # Constant fields settings
        self._pzadrv_psu_update_volts_min_max(VOLTS_BOUNDS["min"], VOLTS_BOUNDS["max"])
        self._pzadrv_psu_update_amps_min_max(AMPS_BOUNDS["min"], VOLTS_BOUNDS["max"])

        # Misc.
        self._pzadrv_psu_update_misc("model", "HM744 (HAMEG)")

        # Call meta class PSU init.
        super()._PZADRV_loop_ini(tree)

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_state_value(self):
        return "on" if self.handle.state(self.channel) else "off"

    def _PZADRV_PSU_write_state_value(self, v):
        status     = STATE_VALUE_ENUM.get(v, False)
        self.state = v
        self.handle.enable(self.channel, status)


    def _PZADRV_PSU_read_volts_value(self):
        return self.handle.volts_get(self.channel)

    def _PZADRV_PSU_write_volts_value(self, v):
        self.handle.volts_set(self.channel, v)

    def _PZADRV_PSU_read_amps_value(self):
        return self.handle.amps_get(self.channel)

    def _PZADRV_PSU_write_amps_value(self, v):
        self.handle.amps_set(self.channel, v)
