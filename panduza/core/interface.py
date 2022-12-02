import time
import json
import paho.mqtt.client as mqtt

from .core import Core
from .client import Client
from .heartbeat import HeartBeatMonitoring

class Interface:

    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None, url=None, port=None, b_topic=None, pza_client=None):
        """Constructor
        """
        self._initialized = False
        self.init(alias, url, port, b_topic, pza_client)

    ###########################################################################
    ###########################################################################

    def _post_initialization(self):
        pass

    ###########################################################################
    ###########################################################################

    def init(self, alias=None, url=None, port=None, b_topic=None, pza_client=None):
        """Initialization of the interface
        """
        # Wait for later initialization
        if alias==None and url==None and port==None and b_topic==None and pza_client==None:
            return

        #
        if pza_client != None:
            self.client = pza_client
            self.base_topic = b_topic

        # Build a new client
        else:
            if alias:
                self.client = Client(interface_alias=alias)
                self.base_topic = Core.BaseTopicFromAlias(alias)
            else:
                self.base_topic = b_topic
                self.client = Client(url=url, port=port)

        # 
        if not self.client.is_connected:
            self.client.connect()

        
        # #
        # self.heart_beat_monitoring = HeartBeatMonitoring(self.client, self.base_topic)
        

        # Initialization ok
        self._initialized = True

        #
        self._post_initialization()

    ###########################################################################
    ###########################################################################

    def payload_to_dict(self, payload):
        """ To parse json payload
        """
        return json.loads(payload.decode("utf-8"))

    ###########################################################################
    ###########################################################################

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

    ###########################################################################
    ###########################################################################

    def enableHeartBeatMonitoring(self):
        """
        """
        print("enableHeartBeatMonitoring ::: DEPRECATED !!!!!!!!!")
        # self.client.subscribe(self.base_topic + "/info")
        # self.HBM = { "alive": False, "enabled": True, "heartbeat": time.time() }

    ###########################################################################
    ###########################################################################

    def disableHeartBeatMonitoring(self):
        print("disableHeartBeatMonitoring ::: DEPRECATED !!!!!!!!!")
        # self.client.unsubscribe(self.base_topic + "/info")
        # self.HBM = { "enabled": False }

    ###########################################################################
    ###########################################################################

    def isAlive(self):
        """
        """
        if not self.heart_beat_monitoring.enabled:
            raise Exception("watchdog not enabled on the interface")
        
        t0 = time.time()
        while (time.time() - t0 < 3) and not self.heart_beat_monitoring.alive:
            pass

        return self.heart_beat_monitoring.alive

    ###########################################################################
    ###########################################################################

    def _on_mqtt_message(self, client, userdata, msg):
        # print("!!!", msg.topic)

        if msg.topic.endswith('/info'):
            self.heart_beat_monitoring.update()

