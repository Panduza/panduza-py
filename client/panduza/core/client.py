"""Simple API for Panduza
 Florian Dupeyron
 February 2022
"""

# from abc import ABC, abstractmethod

import time
from fnmatch import fnmatch

import logging
import threading
import traceback

import json
import queue
import paho.mqtt.client as mqtt

from .core import Core

# ┌────────────────────────────────────────┐
# │ Utilities                              │
# └────────────────────────────────────────┘

# def _pza_path_join(*args):
#     return "/".join(args)

# ┌────────────────────────────────────────┐
# │ Panduza client                         │
# └────────────────────────────────────────┘


class Client:

    def __init__(self, broker_alias=None, interface_alias=None, url=None, port=None):
        """Client Constructor

        The client can be build from

        - Alias
        OR
        - Url + Port

        Args:
            alias (str, optional): connection alias. Defaults to None.
            url (str, optional): broker url. Defaults to None.
            port (str, optional): port url. Defaults to None.
        """
        # Manage double way of loading client information
        if broker_alias:
            self.url, self.port = Core.BrokerInfoFromBrokerAlias(broker_alias)
        elif interface_alias:
            self.url, self.port = Core.BrokerInfoFromInterfaceAlias(
                interface_alias)
        else:
            self.url = str(url)
            self.port = int(port)

        # Set flags
        self.is_connected = False

        # Logs
        self.log = logging.getLogger(f"pza.client:{self.url}:{self.port}")
        self.log.info("Init Client")

        # Init MQTT client instance
        self.client = mqtt.Client()
        self.client.on_message = self.__on_message
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect

        # Listeners
        self._listeners = dict()
        """_listeners
        {
            topics: { wildcard: "string" , callbacks: [
                { "cb":   "kwargs": }
            ] }
            ...
        }
        @todo: should be converted into a class....
        """
        self._listeners_lock = threading.RLock()

    # ┌────────────────────────────────────────┐
    # │ Connect / Disconnect                   │
    # └────────────────────────────────────────┘

    def connect(self):
        self.log.debug("Connect to broker")
        self.client.connect(self.url, self.port)
        self.client.loop_start()

    def disconnect(self):
        self.log.debug("Disconnect from broker")
        self.client.disconnect()
        self.client.loop_stop()

    def __on_connect(self, client, userdata, flags, rc):
        self.is_connected = True
        self.log.debug("Connected!")

    def __on_disconnect(self, client, userdata, rc):
        self.is_connected = False
        self.log.debug("Disconnected!")

    # ┌────────────────────────────────────────┐
    # │ Message callback                       │
    # └────────────────────────────────────────┘

    def __on_message(self, client, userdata, message):
        """Callback triggered when mqtt data are recieved by the client
        """
        # Debug
        self.log.debug(f"Rx topic({message.topic}) data({message.payload})")

        #
        with self._listeners_lock:

            for listener_topic in self._listeners:
                l = self._listeners[listener_topic]

                if fnmatch(message.topic, l["wildcard"]):
                    # Call all listener's callbacks
                    for callback in l["callbacks"]:
                        # self.log.debug(f"- listener notified !")

                        callback["cb"](
                            message.topic, message.payload, **callback["kwargs"])

                # self.log.error(f"Message recieved but no listner registered for this topic {message.topic}")

    # ┌────────────────────────────────────────┐
    # │ Publish wrapper                        │
    # └────────────────────────────────────────┘

    def publish(self, topic, payload: bytes, qos=0):
        """Helper to publish raw messages
        """
        # Debug
        self.log.debug(f"MSG_OUT %{topic}% {payload} QOS={qos}")

        request = self.client.publish(topic, payload, qos=qos, retain=False)
        request.wait_for_publish()


    def publish_json(self, topic, req: dict, qos=0):
        """Helper to publish json messages
        """
        request = self.publish(
            topic=topic,
            payload=json.dumps(req).encode("utf-8"),
            qos=qos
        )

    # ┌────────────────────────────────────────┐
    # │ Register/Unregister listener           │
    # └────────────────────────────────────────┘

    def subscribe(self, topic: str, callback, **kwargs):
        """Registers the listener, returns the queue instance
        """

        with self._listeners_lock:
            self.log.debug(f"Register listener for topic '{topic}'")
            # Create set if not existing for topic
            if not topic in self._listeners:
                self._listeners[topic] = {
                    "wildcard": topic.replace("/+", "/*").replace("/#", "/*"),
                    "callbacks": []
                }
                self.client.subscribe(topic)

            # Check that callback is not already registered, and register
            if callback in self._listeners[topic]["callbacks"]:
                raise ValueError(
                    f"callback {callback} already registered for topic {topic}")

            else:
                self._listeners[topic]["callbacks"].append(
                    {"cb": callback, "kwargs": kwargs})

    # ┌────────────────────────────────────────┐
    # │                                        │
    # └────────────────────────────────────────┘

    def __unsubscribe_from_topic_only(self, topic: str):
        if topic in self._listeners:
            l = self._listeners[topic]

            # Send none value to callbacks to unlock listener if needed
            for callback in l["callbacks"]:
                try:
                    callback["cb"](None, None, **callback["kwargs"])
                except:
                    self.log.error(traceback.format_exc())

            # Remove set from dict (hardcore mode)
            self.client.unsubscribe(topic)
            del self._listeners[topic]

    def __unsubscribe_from_topic_and_callback(self, topic: str, callback):
        if topic in self._listeners:
            l = self._listeners[topic]

            for c in l["callbacks"]:
                if c["cb"] == callback:
                    try:
                        callback(None, None)
                        l["callbacks"].remove(c)
                    except:
                        self.log.error(traceback.format_exc())

            # if no more callback, unsubscribe from mqtt topic and kill listener
            if len(l["callbacks"]) == 0:
                self.client.unsubscribe(topic)
                del self._listeners[topic]

    # ┌────────────────────────────────────────┐
    # │                                        │
    # └────────────────────────────────────────┘

    def unsubscribe(self, topic: str, callback=None):
        """Unsuscribe listener from topic. if callback is None, unregister all listeners
        """

        self.log.debug(f"Unregister listener for topic '{topic}'")

        with self._listeners_lock:
            if callback is None:
                self.__unsubscribe_from_topic_only(topic)
            else:
                self.__unsubscribe_from_topic_and_callback(topic, callback)

    def listeners_number(self):
        n = 0
        with self._listeners_lock:
            for l in self._listeners:
                n += len(self._listeners[l]["callbacks"])
        return n


    ###########################################################################
    ###########################################################################
    #
    # SCAN INTERFACE MANAGEMENT
    #
    ###########################################################################
    ###########################################################################

    def __store_scan_result(self, topic, payload):
        """Callback to store scan results piece by piece
        """
        # lock
        with self.__scan_mutex:

            # Check if topic is valid
            if topic == None:
                return

            # Extract the base topic
            base_topic = topic[:-len("/atts/info")]

            # Check for duplicate
            if base_topic in self.__scan_results:
                return

            # Process the payload
            info = json.loads(payload.decode("utf-8"))
            if info["info"]["type"] == "platform":
                self.__scan_count_platform += info["info"]["interfaces"]
                self.__scan_count_interfaces += 1
            else:
                self.__scan_count_interfaces += 1

            # Push debug logs
            self.__scan_messages_logs.put(info)

            # Store result
            if base_topic not in self.__scan_results and fnmatch(info["info"]["type"], self.__scan_type_filter):
                self.__scan_results[base_topic] = info["info"]

    # ---

    def scan_interfaces(self, type_filter="*"):
        """Scan broker panduza interfaces and return them

        The fast scan is based on the fact that each platform will declare a
        special interface with type *platform*. In the *info* topic of this
        interface there is a special *interfaces* field, it contains the number
        of interface managed by the platfrom. 

        So when you start a scan with * in pza, you create 2 counters
        - one that is incremented (+1) for each interface that respond
        - one that is incremented (+info/interfaces) when an interface *platform* respond

        When both counter are equal, you are sure that you've got all the interfaces
        """
        # Init
        self.__scan_mutex = threading.Lock()
        self.__scan_results = {}
        self.__scan_messages_logs = queue.Queue()
        self.__scan_count_platform = 0
        self.__scan_count_interfaces = 0
        self.__scan_type_filter = type_filter

        # Debug log
        self.log.info("Start Interface Scanning...")

        # Subscribe to interfaces info responses
        self.subscribe("pza/+/+/+/atts/info", self.__store_scan_result)

        # Send the global discovery request and wait for answers
        self.publish("pza", u"*", qos=0)

        # Scanning wait with a 5 secondes timeout
        start_scan_time = time.perf_counter()
        continue_scan = True
        while continue_scan and (time.perf_counter() - start_scan_time < 5):
            time.sleep(0.25)
            with self.__scan_mutex:
                continue_scan = (self.__scan_count_platform == 0) or (self.__scan_count_platform != self.__scan_count_interfaces)

        # Debug logs from the mqtt client thread
        while not self.__scan_messages_logs.empty():
            msg = self.__scan_messages_logs.get()
            self.log.info(msg)

        # cleanup and return
        self.unsubscribe("pza/+/+/+/atts/info")

        # Trigger error when timeout
        if time.perf_counter() - start_scan_time >= 5:
            raise Exception(f"Scan timeout found={self.__scan_count_interfaces}/expected={self.__scan_count_platform}\n\nreceived {self.__scan_results}")

        # 
        self.log.info(f"Scan ok found={self.__scan_count_interfaces}/expected={self.__scan_count_platform}")

        return self.__scan_results

