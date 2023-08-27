import time
#from hamcrest import empty
import serial
from panduza_platform import MetaDriverBpc

class DriverKA005P(MetaDriverBpc):
    """ Driver to manage the HM7044 power supply
    """

    ###########################################################################
    ###########################################################################
    
    def __init__(self):
        self.ovp = False
        self.ocp = False
        self.silent = False
        super().__init__()

    def config(self):
        """ FROM MetaDriver
        """

        return {
            "compatible": "ka3005p",
            "info": { "type": "bpc", "version": "1.0" },
        }
        
    ###########################################################################
    ###########################################################################

    def setup(self, tree):
        """ FROM MetaDriver
        """
        # Initialize variables
        self.supported_settings = self.api_settings.copy()

        self.api_attributes["voltage"]["max"] = 30
        self.api_attributes["voltage"]["scale"] = 0.01

        self.api_attributes["current"]["max"] = 5
        self.api_attributes["current"]["scale"] = 0.001
        
        self.api_attributes["model_name"] = "KA3005P"

        if "settings" not in tree or "serial_port" not in tree["settings"]:
            logger.error("Setting serial_port is mandatory for this driver")
            return False
        self.serial_port = tree["settings"]["serial_port"]
        self.tree_settings = tree["settings"].copy()

        self.__serial = serial.Serial(self.serial_port, 9600, timeout=1)

        # Register commands
        self.bpc_register_command("state", self.__set_state)
        self.bpc_register_command("voltage", self.__set_voltage)
        self.bpc_register_command("current", self.__set_current)
        self.bpc_register_command("settings", self.__set_settings)

        for key in self.tree_settings.copy():
            if key not in self.supported_settings:
                logger.warning("Driver ka3005p does not support setting " + key + " and will ignore it.")
                self.remove_setting(self.supported_settings, key)
            else:
                self.supported_settings[key] = self.tree_settings[key]

        self.api_attributes["settings"] = self.supported_settings

    ###########################################################################
    ###########################################################################

    def on_start(self):
        super().on_start()
        pass

    ###########################################################################
    ###########################################################################
        
    def loop(self):
        """ FROM MetaDriver
        """
        return False

    ###########################################################################
    ###########################################################################

    def __set_state(self, payload):
        """
        """
        req = self.payload_to_dict(payload)
        req_state = req["state"]
        # Update enable
        self.state = req_state
        if self.state == "on":
            cmd = bytearray(b'OUT1')
        elif self.state == "off":
            cmd = bytearray(b'OUT0')
        self.__serial.write(cmd)
        self.bpc_push_attribute("state", self.state)
        logger.info(f"new state :" + str(payload))

    ###########################################################################
    ###########################################################################

    def __set_voltage(self, payload):
        """
        """
        req = self.payload_to_dict(payload)
        self.api_attributes["voltage"]["value"] = req["voltage"]
        print(req["voltage"])
        cmd = bytearray(b'VSET1:') + bytearray(str(req["voltage"]), encoding='utf8')
        self.__serial.write(cmd)
        # Update state
        self.bpc_push_attribute("voltage", self.api_attributes["voltage"])
        logger.info(f"new voltage :" + str(payload))

    ###########################################################################
    ###########################################################################

    def __set_current(self, payload):
        """
        """
        req = self.payload_to_dict(payload)
        self.api_attributes["current"]["value"] = req["current"]
        print(req["current"])
        cmd = bytearray(b'ISET1:') + bytearray(str(req["current"]), encoding='utf8')
        self.__serial.write(cmd)
        # Update state
        self.bpc_push_attribute("current", self.api_attributes["current"])
        logger.info(f"new current :" + str(payload))
        pass

    def __set_settings(self, payload):
        """
        """
        # Parse request
        req = self.payload_to_dict(payload)
        req_settings = req["settings"]
        if req_settings["ovp"] is not self.ovp:
            self.__set_ovp(req_settings["ovp"])
        if req_settings["ocp"] is not self.ocp:
            self.__set_ocp(req_settings["ocp"])
        if req_settings["silent"] is not self.silent:
            self.__set_silent(req_settings["silent"])
        # Update state
        self.settings = req_settings
        self.bpc_push_attribute("settings", self.settings)
        logger.info(f"new settings:" + str(payload))

    def __set_ovp(self, value):
        print("Will set OVP to " + str(value))
        if value == True:
            cmd = bytearray(b'OVP1')
        else:
            cmd = bytearray(b'OVP0')
        self.__serial.write(cmd)
        self.ovp = value

    def __set_ocp(self, value):
        print("Will set OCP to " + str(value))
        if value == True:
            cmd = bytearray(b'OCP1')
        else:
            cmd = bytearray(b'OCP0')
        self.__serial.write(cmd)
        self.ocp = value

    def __set_silent(self, value):
        print("Will set Silent to " + str(value))
        if value == True:
            cmd = bytearray(b'BEEP1')
        else:
            cmd = bytearray(b'BEEP0')
        self.__serial.write(cmd)
        self.silent = value
