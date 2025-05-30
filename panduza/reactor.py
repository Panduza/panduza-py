import threading;
import json
import logging
import paho.mqtt.client as mqtt

from panduza.attributes.notification import NotificationAttribute
from panduza.attributes.vectorf32 import VectorF32Attribute
from .structure import Structure
from .attributes import SiAttribute, StringAttribute, NumberAttribute, EnumAttribute, JsonAttribute, BooleanAttribute, MemoryCommandAttribute, StatusAttribute


class Reactor:

    # ---
    def __init__(self, addr="127.0.0.1", port=1883, namespace=None):
        """
        """
        # Create a logger for reactor
        self.logger = logging.getLogger(__name__)

        self.attributes = dict()

        self.addr = addr
        self.port = port
        self.namespace = namespace

        self.client = mqtt.Client(
            protocol=mqtt.MQTTProtocolVersion.MQTTv311,
        )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.known_platforms = []

        self.pza_structure = Structure()

        self.topic_root = None

        # This event helps 'start' to block until the connection to the broker
        # is really effective
        self._connected_event = threading.Event()
        self._structure_event = threading.Event()
    
    # ---

    def start(self):
        """Start the reactor
        """
        # 
        self.logger.debug(f"starting {self.addr}:{self.port}")

        # Start Connection
        status = self.client.connect(self.addr, self.port)
        if status != mqtt.MQTTErrorCode.MQTT_ERR_SUCCESS:
            self.logger.debug(f"error {status}")
        self.client.loop_start()

        # Wait for connnection to be active
        if self._connected_event.wait(5):
            self.logger.debug(f"connection success")
        else: 
            raise Exception("connection timeout")

        # 
        self.client.subscribe("pza/_/#")

        # 
        self.logger.debug(f"waiting for bench structure")
        if self._structure_event.wait(2):
            self.logger.debug(f"structure ok")
        else: 
            raise Exception("structure not recieved from the bench")

    # ---

    def stop(self):
        """Stop the reactor
        """
        self.client.loop_stop()
        self.client.disconnect()
        self.known_platforms = []
        self.pza_structure = Structure()
        self._connected_event.clear()
        self._structure_event.clear()
    
    # ---

    def attribute_type_str_to_obj(self, type_str):
        if type_str == "si":
            return SiAttribute
        elif type_str == "string":
            return StringAttribute
        elif type_str == "number":
            return NumberAttribute
        elif type_str == "enum":
            return EnumAttribute
        elif type_str == "json":
            return JsonAttribute
        elif type_str == "boolean":
            return BooleanAttribute
        elif type_str == "memory_command":
            return MemoryCommandAttribute
        elif type_str == "vector_f32-v0":
            return VectorF32Attribute
        else:
            raise ValueError(f"Unknown attribute type: {type_str}")

    # ---

    def find(self, xtopic):
        self.logger.debug(f"Searching for attribute '{xtopic}'")

        # Find attribute data
        att_data = self.pza_structure.find_attribute_from_xtopic(xtopic)
        if not att_data:
            raise ValueError(f"Attribute '{xtopic}' not found")
        
        topic = att_data[0]
        type = att_data[1]["type"]
        mode = att_data[1]["mode"]
        settings = att_data[1]["settings"]
        type_obj = self.attribute_type_str_to_obj(type_str=type)
        att = type_obj(reactor=self, topic=topic, mode=mode, settings=settings)
        self.attributes[f"{topic}/att"] = att
        return att

    # ---

    def on_connect(self, client, userdata, flags, rc):
        """Triggered when connection done
        """
        self.logger.debug(f"Connected with result code {str(rc)}")
        self._connected_event.set()

    # ---

    def on_message(self, client, userdata, msg):
        # 
        # self.logger.debug(f"Received message: topic={msg.topic}, payload={str(msg.payload)}")

        # print(msg.topic)

        # layers = msg.topic.split("/")

        if msg.topic == "pza/_/structure/att":
            
            self.pza_structure.update(json.loads(msg.payload.decode('utf-8')))
            # We assurme than we are connected only when the bench structure
            # has been recieved
            self._structure_event.set()

        
        # if len(layers) == 2:
        #     print("scannn !! {}", msg.topic)
        #     self.known_platforms.append(msg.topic)
        
        # print(self.attributes)
        att = self.attributes.get(msg.topic, None)
        if att:
            att.on_att_message(msg.payload)
        # else:
        #     print("nada")
        # if self.is_platform_topic(msg.topic):
        #     self.known_platforms.append(msg.topic)
        # else:
        #     # Handle message payload and trigger on_message event
        #     pass


    # def scan(self):
    #     self.known_platforms = []
    #     self.client.publish("pza", b"*")
    #     time.sleep(1)
        
    #     self.structure = {}
    #     for platform in self.known_platforms:
    #         ttt = f"{platform}/_/structure"
            
    #         a = self.attribute(ttt, None)
    #         a.wait_for_first_value()
    #         # print(f"----------- {a.get()}")
            
    #         device_name = platform.split("/")[1]
            
    #         self.structure[device_name] = a.get()

        # print(self.structure)



    def new_status_attribute(self):
        """
        Create a new status attribute
        """
        topic = "pza/_/status"
        att = StatusAttribute(reactor=self, topic=topic, mode="ro")
        self.attributes[f"{topic}/att"] = att
        return att

    def new_notification_attribute(self):
        """
        Create a new notification attribute
        """
        topic = "pza/_/notifications"
        att = NotificationAttribute(reactor=self, topic=topic, mode="ro")
        self.attributes[f"{topic}/att"] = att
        return att

