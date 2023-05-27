import time
import threading
from ...meta_drivers.io import MetaDriverIo

class DriverIoFake(MetaDriverIo):
    
    ###########################################################################
    ###########################################################################

    def config(self):
        """ From MetaDriver
        """
        return {
            "name": "FakeIO",
            "description": "Virtual IO",
            "compatible": [
                "io_fake",
                "py.io_fake"
            ],
            "info": { "type": "io", "version": "1.0" },
            "settings": {
                "behaviour": { "type": "str", "desc": "fake behaviour of the io [static|auto_toggle]" },
                "loopback": { "type": "str", "desc": "to internaly loopback the value to an other fake_io interface" }
            }
        }
    
    ###########################################################################
    ###########################################################################

    def setup(self, tree):
        """ From MetaDriver
        """
        # Initialize basic properties
        self.direction = 'in'
        self.value=0
        self.behaviour="static"
        self.__loop = 0
        self.loopback = None
        self.mutex = threading.Lock()

        # Configure the fake behaviour
        # Static by default => just wait for commands
        if "settings" in tree:
            settings = tree["settings"]

            #
            if "behaviour" in settings:
                target_behaviour = settings["behaviour"]
                if target_behaviour in ["static", "auto_toggle"]:
                    self.behaviour = target_behaviour
                else:
                    logger.error("unknown behaviour '{}' fallback to 'static'", target_behaviour)

            # 
            if "loopback" in settings:
                self.loopback = self.get_interface_instance_from_name(settings["loopback"])
                logger.info(f"loopback enabled : {self.loopback}")

        # Register commands
        self.register_command("value/set", self.__value_set)
        self.register_command("direction/set", self.__direction_set)

    ###########################################################################
    ###########################################################################

    def on_start(self):
        """On driver start, just update initiale io attributes
        """
        self.push_io_value(self.value)
        self.push_io_direction(self.direction)

    ###########################################################################
    ###########################################################################

    def loop(self):
        """ From MetaDriver
        """
        if self.behaviour == "auto_toggle":
            if self.__loop >= 8:
                self.value = (self.value + 1) % 2
                self.__loop = 0
            self.__loop += 1
            time.sleep(0.25)
            return True
        else:
            return False

    ###########################################################################
    ###########################################################################

    def force_value_set(self, value):
        """To force the set from an other driver
        """
        self.mutex.acquire()
        self.value=value
        self.push_io_value(self.value)
        self.mutex.release()
        logger.info(f"force value : {self.value}")

    ###########################################################################
    ###########################################################################

    def __value_set(self, payload):
        """Apply set value request
        """
        # Parse request
        req = self.payload_to_dict(payload)
        req_value = req["value"]
        # Update value
        self.value=req_value
        self.push_io_value(self.value)
        #
        if self.loopback:
            self.loopback.force_value_set(self.value)
        # log
        logger.info(f"new value : {self.value}")

    ###########################################################################
    ###########################################################################

    def __direction_set(self, payload):
        """Apply set direction request
        """
        # Parse request
        req = self.payload_to_dict(payload)
        req_direction = req["direction"]
        # Update direction
        self.direction=req_direction
        self.push_io_direction(self.direction)
        # log
        logger.info(f"new direction : {self.direction}")
