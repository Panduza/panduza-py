import os
import json
import time
import logging
import threading

from abc import ABC, abstractmethod
from typing      import Optional, Callable, Set
from dataclasses import dataclass, field
from typing      import ClassVar

from .client import Client

from .helper import topic_join

from .log import create_logger

# -----------------------------------------------------------------------------

class EnsureError(Exception):
    """ @brief Error raised when ensure tiemout is reached
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[ERROR] %s\n" % str(self.message)

# -----------------------------------------------------------------------------

@dataclass
class Attribute:
    name: str
    interface = None

    # True if the attribute must be published on mqtt with retain=True
    retain: bool = True

    # Do not wait for attribute update at start (interface may be empty)
    bypass_init_ensure: bool = False

    # Delay before ensure function raise an error (in seconds)
    ENSURE_TIMEOUT: ClassVar[float] = 5.0

    # ---

    def __post_init__(self):
        """Initialize topics and logging
        """
        self.counter = 0

        self._log = create_logger(self.name)
        self._lhead = f"<?.{self.name} {id(self)}>"
        self._log.debug(f"{self._lhead} NEW attribute retain={self.retain}")

        self._field_names = [] # authorized field names

        self._field_data = {}
        self._field_data_lock = threading.Lock()

        self._update_event = threading.Event()
        self._update_event.clear()

    # ---

    def set_interface(self, interface):
        """Attach this attribute to the interface
        """
        # Attach interface
        self.interface = interface
        self._log.debug(f"{self._lhead} attach to interface '{self.interface.get_short_name()}'")
        self._lhead = f"<{self.interface.get_short_name()}.{self.name}>"
        self._topic_atts = topic_join(self.interface.topic, "atts", self.name)
        self._topic_cmds_set = topic_join(self.interface.topic, "cmds", "set")

        # Subscribe to topic
        self._log.debug(f"{self._lhead} subscribe to topic atts : %{self._topic_atts}%")
        self.interface.client.subscribe(self._topic_atts, callback=self._on_att_message)

    # ---

    def ensure_init(self):
        """Ensure that the interface has been initialized by the broker
        """
        # Check by pass
        if self.bypass_init_ensure:
            return
        # Do not need to check if the attribute is not retained
        if not self.retain:
            return
        # Do not need to check the misc attribute (all fields are optionnal)
        if self.name == "misc":
            return

        # Prepare counter
        self._log.debug(f"{self._lhead}ENSURE INIT")
        self._update_event.clear()
        start_time = time.perf_counter()

        while (
            not self._field_data and
            (time.perf_counter()-start_time) < Attribute.ENSURE_TIMEOUT
            ):
            remaining_time = Attribute.ENSURE_TIMEOUT - (time.perf_counter()-start_time)
            # self._log.debug(f'remaining {remaining_time:0.6f} seconds')
            self._update_event.wait(remaining_time)

        if time.perf_counter()-start_time >= Attribute.ENSURE_TIMEOUT:
            raise EnsureError(f"{self._lhead} initial data not recieved for attribute '{self.name}'")

    # ---
    
    def _on_att_message(self, topic, payload):
        """Triggered when a new message is received

        !!! WORK ON MQTT CLIENT THREAD !!!
        """
        # Debug
        self._log.debug(f"{self._lhead}MSG_IN < %{topic}% {payload}")

        # Parse
        payload_dict = json.loads(payload.decode("utf-8"))

        # Control
        if self.name not in payload_dict:
            self._log.warning(f"{self._lhead}bad format for attribute payload")
            return

        # Update
        field_update = payload_dict.get(self.name, {})
        with self._field_data_lock:
            for field, update in field_update.items():
                self._field_data[field] = update
                self._log.debug(f"{self._lhead}UPDATE < {field}={self._field_data[field]}")
                # self._log.debug(f"{self._lhead}ALL FIELDS < {self._field_data}")
                
        # Thread trigger
        self._update_event.set()

    # ---

    def add_field(self, field):
        """Append a field to the attribute
        """
        field.set_attribute(self)
        setattr(self, field.name, field)
        with self._field_data_lock:
            self._field_names.append(field.name)
        return self
    
    # ---

    def support(self, field_name):
        if field_name in self._field_data:
            return True
        else:
            return False

    # ---

    def get(self, field):
        """Return the value localy stored
        """
        with self._field_data_lock:
            if not (field in self._field_names):
                self._log.warning(f"{self._lhead} has no field {field}")
                return None
            # self._log.debug(f"{self._lhead} get('{field}') {type(self._field_data)} {self._field_data[field]}")
            return self._field_data.get(field)

    # ---

    def set(self, **kwargs):
        """Send a set command
        """
        # Get ensure flag
        ensure=kwargs.get('ensure', True)

        # Prepare the payload
        kwargs.pop('ensure', None)
        pyl={}
        for key, value in kwargs.items():
            # TODO Check if the key match a field name
            pyl[key] = value
        cmd={}
        cmd[self.name] = pyl

        # Send message
        self.interface.client.publish_json(self._topic_cmds_set, cmd)

        # If ensure flag is set, wait for it
        if ensure:
            self._update_event.clear()
            start_time = time.perf_counter()
            self._log.debug(f'wait to ensure the request is applied')

            while (
                not self.update_ack(kwargs) and
                (time.perf_counter()-start_time) < Attribute.ENSURE_TIMEOUT
                ):

                remaining_time = Attribute.ENSURE_TIMEOUT - (time.perf_counter()-start_time)
                self._log.debug(f'remaining {remaining_time:0.6f} seconds')
                self._update_event.wait(remaining_time)

            if time.perf_counter()-start_time >= Attribute.ENSURE_TIMEOUT:
                raise EnsureError(f"client did not recieved a correct answer when changing attributes {self._lhead} with {kwargs}")

    # ---

    def update_ack(self, expected_data):
        """Control if the internal data match the expected one by the user
        """
        # debug
        self._log.debug(f'update_ack expected={expected_data} recieved={self._field_data}')

        # Control
        for key, value in expected_data.items():
            if (key not in self._field_data) or (self._field_data[key] != value):
                # self._log.debug(f'NOK')
                return False

        # Ok if no diff found
        # self._log.debug(f'ok')
        return True

###############################################################################
###############################################################################

@dataclass
class Attribute_JSON(Attribute):
    __value: any = None

    def __post_init__(self):

        print("!!! DEPRECATED Attribute_JSON !!!")
        super().__post_init__()

        self.__trigger = threading.Event()

        # Subscribe to topic
        self.client.subscribe(self._topic_atts_get, callback=self.__update)


    def __del__(self):
        # Unsubscribe from topic
        self.client.unsubscribe(self._topic_atts_get, callback=self.__update)

    # ┌────────────────────────────────────────┐
    # │ Update callback                        │
    # └────────────────────────────────────────┘

    def __update(self, topic, payload):
        self._log.debug("Received new value")

        if payload is None:
            self.__value = None
        else:
            self.__value = self.payload_parser(payload)
            self.__trigger.set()
    

    # ┌────────────────────────────────────────┐
    # │ Trigger control                        │
    # └────────────────────────────────────────┘
    
    def trigger_arm(self):
        self.__trigger.clear()

    def trigger_wait(self, timeout):
        try:
            self.__trigger.wait(timeout=timeout)
        except:
            pass

    # ┌────────────────────────────────────────┐
    # │ Set/get                                │
    # └────────────────────────────────────────┘

    def get(self):
        return self.__value

    def set(self, v, ensure=False):
        """Set the attribute

        Args:
            v (_type_): The new value
            ensure (bool, optional): Set to true to wait for the confirmation that the command has been executed. Defaults to False.
        """

        retry=3
        if ensure:
            self.trigger_arm()

        self.client.publish(self._topic_cmds_set, self.payload_factory(v))

        if ensure:
            # It is possible that you catch some initialization message with the previous dir value
            # To manage this case, just wait for the correct value
            while self.__value != v and retry > 0:
                self.trigger_wait(timeout=1)
                if self.__value != v:
                    self.trigger_arm()
                    retry-=1

            if self.__value != v:
                raise RuntimeError(f"Attribute {self.name} for {self.base_topic}: cannot set to '{v}', got '{self.__value}'")


