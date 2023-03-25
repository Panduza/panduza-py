import time
import json
import paho.mqtt.client as mqtt

from dataclasses import dataclass, field

from .core import Core
from .client import Client
from .helper import topic_join

from .attribute_info import AttributeInfo
from .log import create_logger

@dataclass
class Interface:
    """Access point to a Panduza interface
    """

    alias : str = None
    addr : str = None
    port : int = None
    topic : str = None
    client : object = None
    ensure: bool = True

    def __post_init__(self):
        """Constructor
        """
        # Log information
        self._log = create_logger(self.get_short_name())
        self._lhead = f"<{self.get_short_name()}>"
        
        # authorized attribute names
        self._attribute_names = []

        # Try to init the interface
        self.initialized = False
        if( self.init(self.alias, self.addr, self.port, self.topic, self.client) ):
            # === INFO ===
            self.add_attribute( AttributeInfo() )
            self.initialized = True

    # ---

    def init(self, alias=None, addr=None, port=None, topic=None, client=None):
        """Initialization of the interface

        **MUST BE KEPT FOR LATE INIT**

        TODO REWORK NEED TO BE DONE HERE
        """
        # Init Check
        if self.initialized:
            self._log.warning(f"{self._lhead} try to init this interface again")
            return False

        # Wait for later initialization
        if alias==None and addr==None and port==None and topic==None and client==None:
            self._log.warning(f"{self._lhead} cannot initialize interface no parameter provided")
            return False

        #
        if client != None:
            self.client = client
            self.topic = topic

        # Build a new client
        else:
            if alias:
                self.client = Client(interface_alias=alias)
                self.topic  = Core.BaseTopicFromAlias(alias)
                self._log.debug(f"{self._lhead} NEW interface from alias %{self.topic}%")
            elif topic:
                self.topic  = topic
                self.client = Client(url=addr, port=port)
                self._log.debug(f"{self._lhead} NEW interface from topic %{self.topic}%")

        # Connection
        if not self.client.is_connected:
            self.client.connect()

        # Ok init
        return True

    # ---

    def ensure_init(self):
        """Ensure that the interface has been initialized by the broker
        """
        for att in self._attribute_names:
            obj = getattr(self, att)
            obj.ensure_init()

    # ---

    def get_short_name(self):
        if self.alias:
            return self.alias
        else:
            return self.topic.split('/')[-1]

    # ---

    def add_attribute(self, attribute):
        """Append attribute to this interface only once
        """
        if not (attribute.name in self._attribute_names):
            self._log.debug(f"{self._lhead} append {attribute} to {self._attribute_names}")
            self._attribute_names.append(attribute.name)
            attribute.set_interface(self)
            setattr(self, attribute.name, attribute)
        return attribute

    # ---

    def payload_to_dict(self, payload):
        """ To parse json payload
        """
        return json.loads(payload.decode("utf-8"))

    # ---

    def payload_to_int(self, payload):
        """
        """
        return int(payload.decode("utf-8"))

    ###########################################################################
    ###########################################################################

    def payload_to_str(self, payload):
        """
        """
        return payload.decode("utf-8")

    # ###########################################################################
    # ###########################################################################

    # def isAlive(self):
    #     """
    #     """
    #     if not self.heart_beat_monitoring.enabled:
    #         raise Exception("watchdog not enabled on the interface")
        
    #     t0 = time.time()
    #     while (time.time() - t0 < 3) and not self.heart_beat_monitoring.alive:
    #         pass

    #     return self.heart_beat_monitoring.alive

    ###########################################################################
    ###########################################################################

    # def _on_info_message(self, client, userdata, msg):
    #     print("!!!", msg.topic)

        # if msg.topic.endswith('/info'):
        #     self.heart_beat_monitoring.update()

