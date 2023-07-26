import time
import serial
from panduza_platform import MetaDriverBps

class DriverHm7044(MetaDriverBps):
    """ Driver to manage the HM7044 power supply
    """

    ###########################################################################
    ###########################################################################
    
    def config(self):
        """ FROM MetaDriver
        """
        return {
            "compatible": "bps_hm7044",
            "info": { "type": "bps", "version": "1.0" },
            "settings": {
                "serial_port" : "Serial port on which the power supply is connected",
                "channel" : "Channel number that must be driven by this interfaces [1,2,3,4]"
            }
        }
        
    ###########################################################################
    ###########################################################################

    def setup(self, tree):
        """ FROM MetaDriver
        """
        # Initialize variables
        self.serial_port = tree["settings"]["serial_port"]
        self.channel = tree["settings"]["channel"]

        #
        self.enable=False
        self.volts=0
        self.amps=0

        # 
        # self.__serial = serial.Serial(self.serial_port, 9600, timeout=1)

        # Register commands
        self.register_command("enable/set", self.__set_enable)
        self.register_command("volts/set", self.__set_volts)
        self.register_command("amps/set", self.__set_amps)

    ###########################################################################
    ###########################################################################

    def on_start(self):
        #
        # self.push_io_value(self.value)
        pass

    ###########################################################################
    ###########################################################################
        
    def loop(self):
        """ FROM MetaDriver
        """
        # if self._loop % 2 == 0:
        #     self.__push_attribute_value()
        #     self.__push_attribute_direction()
        # self._loop += 1
        # time.sleep(0.5)
        return False

    ###########################################################################
    ###########################################################################

    def __set_enable(self, payload):
        """
        """
        # Parse request
        req = self.payload_to_dict(payload)
        req_enable = req["enable"]
        self.enable=req_enable

        try:
                        
            # message_on = bytearray(b'EN\r\n')
            # read_v = bytearray(b'\r\n')
            # ser.write(message_on)

            # Update mqtt
            self.push_power_supply_enable(self.enable)

            # log
            logger.info(f"new enable : {self.enable}")

        except IOError as e:
            # mogger.error("Unable to set value %s to GPIO %s (%s) | %s", str(val), self.id, path, repr(e))
            pass

    ###########################################################################
    ###########################################################################

    def __set_volts(self, payload):
        """
        """
        # Parse request
        req = self.payload_to_dict(payload)
        req_volts = req["volts"]
        self.volts=req_volts

        try:
                        
            # message_on = bytearray(b'EN\r\n')
            # read_v = bytearray(b'\r\n')
            # ser.write(message_on)

            # Update mqtt
            self.push_power_supply_volts(self.volts)

            # log
            logger.info(f"new volts : {self.volts}")

        except IOError as e:
            # mogger.error("Unable to set value %s to GPIO %s (%s) | %s", str(val), self.id, path, repr(e))
            pass

    ###########################################################################
    ###########################################################################

    def __set_amps(self, payload):
        """
        """
        # Parse request
        req = self.payload_to_dict(payload)
        req_amps = req["amps"]
        self.amps=req_amps

        try:

            # message_on = bytearray(b'EN\r\n')
            # read_v = bytearray(b'\r\n')
            # ser.write(message_on)

            # Update mqtt
            self.push_power_supply_amps(self.amps)

            # log
            logger.info(f"new amps : {self.amps}")

        except IOError as e:
            # mogger.error("Unable to set value %s to GPIO %s (%s) | %s", str(val), self.id, path, repr(e))
            pass


