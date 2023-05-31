import abc
import sys
import time
import json
import asyncio
import traceback
import threading
import paho.mqtt.client as mqtt
import logging

from .log.client import client_logger

from .platform_worker import PlatformWorker

# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================

class AsyncioHelper:
    """Helper provided by paho to execute the client inside an event loop
    """
    def __init__(self, loop, client, log):
        self.log = log
        self.loop = loop
        self.client = client
        self.client.on_socket_open = self.on_socket_open
        self.client.on_socket_close = self.on_socket_close
        self.client.on_socket_register_write = self.on_socket_register_write
        self.client.on_socket_unregister_write = self.on_socket_unregister_write

    def on_socket_open(self, client, userdata, sock):
        self.log.debug("Socket opened")

        def cb():
            self.log.debug("Socket is readable, calling loop_read")
            client.loop_read()

        self.loop.add_reader(sock, cb)
        self.misc = self.loop.create_task(self.misc_loop())

    def on_socket_close(self, client, userdata, sock):
        self.log.debug("Socket closed")
        self.loop.remove_reader(sock)
        self.misc.cancel()

    def on_socket_register_write(self, client, userdata, sock):
        self.log.debug("Watching socket for writability.")

        def cb():
            self.log.debug("Socket is writable, calling loop_write")
            client.loop_write()

        self.loop.add_writer(sock, cb)

    def on_socket_unregister_write(self, client, userdata, sock):
        self.log.debug("Stop watching socket for writability.")
        self.loop.remove_writer(sock)

    async def misc_loop(self):
        self.log.debug("misc_loop started")
        while self.client.loop_misc() == mqtt.MQTT_ERR_SUCCESS:
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
        self.log.debug("misc_loop finished")

# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================

class TopicCallbacks:

    def __init__(self, wildcard) -> None:
        self.wildcard = wildcard
        self.callbacks = []

    def append_callback(self, callback, **kwargs):
        # Check that callback is not already registered, and register
        if callback in self.callbacks:
            raise ValueError(
                f"callback {callback} already registered for topic {self.wildcard}")

        # Append callback
        self.callbacks.append({"cb": callback, "kwargs": kwargs})

# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================

class TopicListeners:

    def __init__(self) -> None:
        self.topic_listeners = []

    def get_entry_from_topic(self, topic):
        """
        """
        # Compose the wildcard from the topic
        wildcard = topic.replace("/+", "/*").replace("/#", "/*")

        # Check that the new wildcard is not already in the store
        for tl in self.topic_listeners:
            if tl.wildcard == wildcard:
                return tl, False

        # Append a new topic listeners
        entry = TopicCallbacks(wildcard)
        self.topic_listeners.append(entry)

        return entry, True

# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================

class PlatformClient(PlatformWorker):
    """Mqtt Client used by the platform and compatible with PlatformThreads
    """

    # ---

    def __init__(self, addr, port) -> None:
        """Constructor
        """
        super().__init__()

        # Save address and port
        self.__addr = addr
        self.__port = port
        self.log = client_logger(str(addr) + ":" + str(port))

        # Mqtt connection
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.__on_message

        # Initialize state
        self.__state = "init"
        self.__state_prev = None

        # States
        self.__states = {
            'init': self.__state_init,
            'run': self.__state_run,
            'err': self.__state_err
        }

        # Topic listeners will store callbacks that must be triggered when
        # a message for a given topic arrive.
        self.__listeners_store = TopicListeners()

    # ---

    def subscribe(self, topic: str, callback, **kwargs):
        """Registers a listener
        """
        # Debug log
        self.log.debug(f"Register listener for topic '{topic}'")

        # Create set if not existing for topics
        entry, new_created = self.__listeners_store.get_entry_from_topic(topic)
        if new_created:
            self.mqtt_client.subscribe(topic)

        # Append callback to the listener
        entry.append_callback(callback, **kwargs)

    # ---

    async def publish(self, topic, payload: bytes, qos=0, retain=False):
        """Helper to publish raw messages
        """
        # Debug
        self.log.debug(f"MSG_OUT %{topic}% {payload} QOS={qos}")

        # Publish the message and wait for it to be complete
        request = self.mqtt_client.publish(topic, payload, qos=qos, retain=retain)

        # Wait for publish but async way
        while(not request.is_published):
            asyncio.sleep(0.01)

        # Debug
        self.log.debug(f"MSG_OUT OK")

    # ---

    async def publish_json(self, topic, req: dict, qos=0, retain=False):
        """Helper to publish json messages
        """
        await self.publish(
            topic=topic,
            payload=json.dumps(req).encode("utf-8"),
            qos=qos,
            retain=retain
        )




    # ---

    def PZA_WORKER_on_thread_attach(self, loop):
        """Triggered when a thread is attached to this worker
        """

        # Create the async loop runner
        self.mqtt_asynch = AsyncioHelper(loop, self.mqtt_client, self.log)

    # ---

    async def _PZA_WORKER_task(self, loop):
        """
        """
        # Log state transition
        if self.__state != self.__state_prev:

            # Managed message
            self._state_started_time = time.time()
            self.log.debug(f"STATE CHANGE ::: {self.__state_prev} => {self.__state}")
            self.__state_prev = self.__state


        # Execute the correct callback
        if not (self.__state in self.__states):
            # error critique !
            pass
        await self.__states[self.__state]()

    # ---

    def __on_message(self, client, userdata, msg):
        """Callback to manage incomming mqtt messages

        Args:
            - client: from paho.mqtt.client
            - userdata: from paho.mqtt.client
            - msg: from paho.mqtt.client
        """
        # Get the topix string
        topic_string = str(msg.topic)

        # Debug purpose
        self.log.debug(f"MSG_IN < %{topic_string}% {msg.payload}")

        # # Check if it is a discovery request
        # if topic_string == "pza":
        #     # If the request is for all interfaces '*'
        #     if msg.payload == b'*':
        #         self.log.info("scan request received !")
        #         self._push_attribute("info", 0, False) # heartbeat_pulse
        #     # Else check if it is specific, there is an array in the payload
        #     else:
        #         # TODO
        #         pass
        #         # try:
        #         #     specifics = self.payload_to_dict(msg.payload)
        #         # except:
        #         #     pass
        #     return

        # # Route to the handle for the command set
        # suffix = topic_string[self.topic_cmds_size:]
        # if suffix == "set":
        #     self._PZADRV_cmds_set(msg.payload)

    # ---

    async def __state_init(self):
        """
        """

        # Start connection
        self.mqtt_client.connect(self.__addr, self.__port)
        
        # Paho recommend to run the client in a separate thread
        # self.mqtt_client.loop_start()
        
        self._init_success()

        # try:
        #     self._PZA_DRV_loop_init(self._tree)
        # except Exception as e:
        #     self._pzadrv_error_detected(str(e) + " " + traceback.format_exc())

    # ---

    async def __state_run(self):
        """
        """
        pass
        

        # try:
        #     self._PZADRV_loop_run()
        # except Exception as e:
        #     self._pzadrv_error_detected(str(e) + " " + traceback.format_exc())

    # ---

    async def __state_err(self):
        """
        """
        pass
        # try:
        #     self._PZADRV_loop_err()
        # except Exception as e:
        #     self.log.error(str(e))

    # ---

    def _init_success(self):
        self.__state = "run"
