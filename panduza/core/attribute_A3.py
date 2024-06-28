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
class AttributeA3:
    name_: str
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

        self._log = create_logger(self.name_)
        self._lhead = f"<?.{self.name_} {id(self)}>"
        self._log.debug(f"{self._lhead} NEW attribute retain={self.retain}")


        self._data = None
        # self._field_data_lock = threading.Lock()

        self._update_event = threading.Event()
        self._update_event.clear()

        self._event_listeners = []

    # ---

    def attach_event_listener(self, callback):
        self._event_listeners.append(callback)

    # ---

    def detach_event_listener(self, callback):
        self._event_listeners.remove(callback)

    # ---

    def set_interface(self, interface):
        """Attach this attribute to the interface
        """
        # Attach interface
        self.interface = interface
        self._log.debug(f"{self._lhead} attach to interface '{self.interface.get_short_name()}'")
        self._lhead = f"<{self.interface.get_short_name()}.{self.name_}>"
        self._topic_atts = topic_join(self.interface.topic, "atts", self.name_)
        # self._topic_cmds_set = topic_join(self.interface.topic, "cmds", "set")

        # Subscribe to topic
        self._log.debug(f"{self._lhead} subscribe to topic atts : %{self._topic_atts}%")
        self.interface.client.subscribe(self._topic_atts, callback=self._on_att_message)


    # ---
    
    def _on_att_message(self, topic, payload):
        """Triggered when a new message is received

        !!! WORK ON MQTT CLIENT THREAD !!!
        """
        # Debug
        self._log.debug(f"{self._lhead}MSG_IN < %{topic}% {payload}")
        self._log.debug(f"{self.name_}")

        # Parse
        # payload_dict = json.loads(payload.decode("utf-8"))

        # Control
        # if self.name_ not in payload_dict:
        #     self._log.warning(f"{self._lhead}bad format for attribute payload")
        #     return
        self._data = payload
        # # Update
        # field_update = payload_dict.get(self.name_, {})
        # with self._field_data_lock:
        #     for field, update in field_update.items():
        #         self._field_data[field] = update
        #         self._log.debug(f"{self._lhead}UPDATE < {field}={self._field_data[field]}")
        #         # self._log.debug(f"{self._lhead}ALL FIELDS < {self._field_data}")

        # Notify listener
        for callback in self._event_listeners:
            callback(payload)

        # Thread trigger
        self._update_event.set()

    # ---

    def get(self):
        """Return the value localy stored
        """
        return self._data

    # ---

    # def set(self, **kwargs):
    #     """Send a set command
    #     """
    #     # Get ensure flag
    #     ensure=kwargs.get('ensure', True)

    #     # Prepare the payload
    #     kwargs.pop('ensure', None)
    #     pyl={}
    #     for key, value in kwargs.items():
    #         # TODO Check if the key match a field name
    #         pyl[key] = value
    #     cmd={}
    #     cmd[self.name_] = pyl

    #     # Send message
    #     self.interface.client.publish_json(self._topic_cmds_set, cmd)

    #     # If ensure flag is set, wait for it
    #     if ensure:
    #         self._update_event.clear()
    #         start_time = time.perf_counter()
    #         self._log.debug(f'wait to ensure the request is applied')

    #         while (
    #             not self.update_ack(kwargs) and
    #             (time.perf_counter()-start_time) < Attribute.ENSURE_TIMEOUT
    #             ):

    #             remaining_time = Attribute.ENSURE_TIMEOUT - (time.perf_counter()-start_time)
    #             self._log.debug(f'remaining {remaining_time:0.6f} seconds')
    #             self._update_event.wait(remaining_time)

    #         if time.perf_counter()-start_time >= Attribute.ENSURE_TIMEOUT:
    #             raise EnsureError(f"client did not recieved a correct answer when changing attributes {self._lhead} with {kwargs}")

    # ---

    # def update_ack(self, expected_data):
    #     """Control if the internal data match the expected one by the user
    #     """
    #     # debug
    #     self._log.debug(f'update_ack expected={expected_data} recieved={self._field_data}')

    #     # Control
    #     for key, value in expected_data.items():
    #         if (key not in self._field_data) or (self._field_data[key] != value):
    #             # self._log.debug(f'NOK')
    #             return False

    #     # Ok if no diff found
    #     # self._log.debug(f'ok')
    #     return True

