import abc
import sys
import time
import json
import asyncio
import traceback
import threading
import paho.mqtt.client as mqtt
import logging

from .log.driver import driver_logger

class MetaDriver(metaclass=abc.ABCMeta):
    """Mother class for all the python meta drivers

    **Execution order**

    - initialize (called by the meta_platform, from the main thread)
    """

    # Time in error state before trying a restart of the interface
    ERROR_TIME_BEFORE_RETRY_S = 10

    ###########################################################################
    ###########################################################################

    def hunt(self):
        """
        """
        config = self._PZADRV_config()
        name = "unnamed" if "name" not in config else config["name"]
        description = "" if "description" not in config else config["description"]
        template = self._PZADRV_tree_template()
        instances = self._PZADRV_hunt_instances()
        obj = {
            "name": name,
            "description": description,
            "template": template,
            "instances": instances
        }
        return obj

    ###########################################################################
    ###########################################################################

    def initialize(self, platform, machine, broker, tree):
        """Post initialization
        """
        # Basics
        self._platform = platform
        self._machine = machine
        self._broker = broker
        self._tree = tree

        # Store attribute representation
        # Contains all the attributes and fields of the driver class in dict
        self.__drv_atts = { }

        # Current state of the driver
        self.__drv_state = 'init'
        self.__drv_state_prev = None

        # Time where the state started
        self._state_started_time = 0

        # Check for name in the driver tree
        if not ("name" in self._tree):
            raise Exception("Name of the interface is required !")

        # Init name and logger
        self._name = self._tree["name"]
        self.log = driver_logger(self._name)

        # Check for name in the driver tree
        if not ("info" in self._PZADRV_config()):
            raise Exception("Config must have *info* in there *_PZADRV_config*")

        # Info attribute
        self.__drv_atts["info"] = self._PZADRV_config()["info"]
        
        # Topic base
        group_name = self._tree["driver"]
        if "group" in self._tree:
            group_name = self._tree["group"]
        self.topic = "pza/" + self._machine + "/" + group_name + "/" + self._name
        self.topic_size = len(self.topic)

        # cmds
        self.topic_cmds = self.topic + "/cmds/"
        self.topic_cmds_size = len(self.topic_cmds)

        # atts
        self.topic_atts = self.topic + "/atts/"
        self.topic_atts_size = len(self.topic_atts)
        self.topic_atts_info = self.topic_atts + "info"

    ###########################################################################
    ###########################################################################

    def start(self):
        """Start the driver engine
        """
        # Mqtt connection
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.__on_message

        try:
            # log
            self.log.info("Interface starting...")

            # Keep alive flag
            self.alive = True

            # Start connection
            self.mqtt_client.connect(self._broker.addr, self._broker.port)

            # Start the mqtt client
            self.mqtt_client.loop_start()

            #
            self.__subscribe_topics()

            # Create an event loop and start the driver
            self.evloop = asyncio.new_event_loop()
            self.evloop.run_until_complete(self.__run_state_machine())

        # except AttributeError as err:
        #     mog.error("Critical error on the serial interface %s (%s)" % (self._name, err))
        # except ConnectionRefusedError as err:
        #     mog.error("Critical error on the driver, MQTT connection failed %s (%s)" % (self._name, err))
        #     mog.error("- you can check if the port %d is open on the broker %s" % (self.bridge.port, self.bridge.port))
        except:
            e = sys.exc_info()[0]
            self.log.exception("Critical error on driver %s (%s)" % (self._name, e))

        # Info
        logging.info("Interface '{}' stopped !", self._name)

    ###########################################################################
    ###########################################################################

    def stop(self):
        """Request to stop the driver thread
        """
        # log
        self.log.info("Stop requested !")
        # Keep alive flag
        self.alive = False

    ###########################################################################
    ###########################################################################

    async def __run_state_machine(self):
        """Core of the state machine
        """
        # log
        self.log.info("Interface started!")

        # States
        __states = {
            'init': self.__drv_state_init,
            'run': self.__drv_state_run,
            'err': self.__drv_state_err
        }

        # Main loop
        while self.alive:
            # Log state transition
            if self.__drv_state != self.__drv_state_prev:
                self._state_started_time = time.time()
                self.log.debug(f"STATE CHANGE ::: {self.__drv_state_prev} => {self.__drv_state}")
                self.__drv_state_prev = self.__drv_state
                # Manage the errstring
                if self.__drv_state == "err":
                    self.log.error(f"ERROR ::: {self.__err_string}")
                    self._update_attribute("info", "error", self.__err_string, False)
                else:
                    self._remove_attribute_field("info", "error", False)
                # update the state
                self._update_attribute("info", "state", self.__drv_state)

            # Execute the correct callback
            if not (self.__drv_state in __states):
                # error critique !
                pass
            await __states[self.__drv_state]()
            
            #
            time.sleep(0.001)

    ###########################################################################
    ###########################################################################

    async def __drv_state_init(self):
        """
        """
        try:
            self._PZADRV_loop_init(self._tree)
        except Exception as e:
            print(traceback.format_exc())
            self._pzadrv_error_detected(str(e))

    async def __drv_state_run(self):
        """
        """
        try:
            self._PZADRV_loop_run()
        except Exception as e:
            print(traceback.format_exc())
            self._pzadrv_error_detected(str(e))

    async def __drv_state_err(self):
        """
        """
        try:
            self._PZADRV_loop_err()
        except Exception as e:
            self.log.error(str(e))

    ###########################################################################
    ###########################################################################

    def __subscribe_topics(self):
        """Subscribe to the required topics
        """
        # Register the common discovery topic 'pza'
        self.mqtt_client.subscribe("pza")
        # Register to all commands
        self.mqtt_client.subscribe(self.topic_cmds + "#")

    ###########################################################################
    ###########################################################################
    
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

        # Check if it is a discovery request
        if topic_string == "pza":
            # If the request is for all interfaces '*'
            if msg.payload == b'*':
                self.log.info("scan request received !")
                self._push_attribute("info", 0, False) # heartbeat_pulse
            # Else check if it is specific, there is an array in the payload
            else:
                # TODO
                pass
                # try:
                #     specifics = self.payload_to_dict(msg.payload)
                # except:
                #     pass
            return
        
        # Route to the handle for the command set
        suffix = topic_string[self.topic_cmds_size:]
        if suffix == "set":
            self._PZADRV_cmds_set(msg.payload)

    ###########################################################################
    ###########################################################################

    def _update_attribute(self, attribute, field, value, push='on-change', retain = True):
        """Function that update only one attribute field

        Args
            - push:
                - 'on-change' [default]: To push only when value of the attribute changed
                - 'always': To always push, even if the value did not change

        Returns
            - True: if the attribute has been updated (means that the internal
                object, holding the attribute, has been updated)
            - False: else
        """
        # Create attribute if not exist
        if not ( attribute in self.__drv_atts ):
            self.__drv_atts[attribute] = dict()

        # Update only if the value changed
        # Then push only if requested
        __att = self.__drv_atts[attribute]
        if not (field in __att) or __att[field] != value:
            __att[field] = value
            if push == 'on-change':
                self._push_attribute(attribute, retain=retain)
            return True

        # Push anyway if the 'push' flag is set to 'always'
        if push == 'always':
            self._push_attribute(attribute, retain=retain)

        # Attribute not updated
        return False

    # ---

    def _update_attributes_from_dict(self, change_dict, push=True, retain = True):
        """Function that update multiple attribute and field at the same time
        """
        for attribute in change_dict:
            modification = False
            for field, value in change_dict[attribute].items():
                modification = self._update_attribute(attribute, field, value, False) or modification
            if push and modification:
                self._push_attribute(attribute, retain=retain)

    # ---

    def _get_field(self, attribute, field):
        """To read a specific field value
        """
        return self.__drv_atts[attribute][field]

    ###########################################################################
    ###########################################################################

    def _remove_attribute_field(self, attribute, field, push=True, retain = True):
        """
        """
        # no attribute or no field with this name
        if not ( attribute in self.__drv_atts ):
            return
        if not ( field in self.__drv_atts[attribute] ):
            return
        # delete the field
        self.__drv_atts[attribute].pop(field)
        # Push if requested
        if push:
            self._push_attribute(attribute, retain=retain)

    ###########################################################################
    ###########################################################################

    def _push_attribute(self, attribute, qos = 0, retain = True):
        """Publish the attribute

        Args
            - retain: True by default because most attribute need it
        """
        # Check for retain
        do_retain=retain
        if do_retain and attribute == "info":
            do_retain=False

        # topic
        topic = self.topic_atts + attribute

        # Payload
        pdict = dict()
        pdict[attribute] = self.__drv_atts.get(attribute, dict())
        payload = json.dumps(pdict)

        # Debug purpose
        self.log.debug(f"MSG_OUT > %{topic}% {payload} retain={do_retain}")

        # Publish
        self.mqtt_client.publish(topic, payload, qos=qos, retain=do_retain)

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

    def get_interface_instance_from_name(self, name):
        """
        """
        return self._platform.get_interface_instance_from_name(name)

    ###########################################################################
    ###########################################################################
    #
    # FOR SUBCLASS USE ONLY
    #
    ###########################################################################
    ###########################################################################

    def _pzadrv_init_success(self):
        self.__drv_state = "run"

    # ---

    def _pzadrv_error_detected(self, err_string):
        self.__drv_state = "err"
        self.__err_string = err_string

    # ---

    def _pzadrv_restart(self):
        self.__drv_state = "init"

    ###########################################################################
    ###########################################################################
    #
    # TO OVERRIDE IN SUBCLASS
    #
    ###########################################################################
    ###########################################################################

    @abc.abstractmethod
    def _PZADRV_config(self):
        """
        """
        pass

    def _PZADRV_tree_template(self):
        """
        """
        return {}

    def _PZADRV_hunt_instances(self):
        """
        """
        return []

    @abc.abstractmethod
    def _PZADRV_loop_init(self, tree):
        """
        """
        pass

    @abc.abstractmethod
    def _PZADRV_loop_run(self):
        """
        """
        pass

    def _PZADRV_loop_err(self):
        """
        """
        elasped = time.time() - self._state_started_time
        if elasped > MetaDriver.ERROR_TIME_BEFORE_RETRY_S:
            self._pzadrv_restart()
        else:
            time.sleep(1)
            self.log.debug(f"restart in { int(MetaDriver.ERROR_TIME_BEFORE_RETRY_S - elasped) }s")

    @abc.abstractmethod
    def _PZADRV_cmds_set(self, payload):
        """Must apply the command on the driver
        """
        pass

