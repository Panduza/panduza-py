import abc
import sys
import time
import json
import queue
import asyncio
import traceback
import threading
import paho.mqtt.client as mqtt
import logging

from .log.driver import driver_logger

from .platform_worker import PlatformWorker

class PlatformDriver(PlatformWorker):
    """Mother class for all the python drivers
    """

    # Time in error state before trying a restart of the interface
    ERROR_TIME_BEFORE_RETRY_S = 10


    def __init__(self) -> None:
        self._pclient = None
        self.__err_string = ""
        super().__init__()

    # =============================================================================
    # PUBLIC FUNCTIONS

    # ---

    def set_platform(self, platform):
        self._platform = platform

    # ---

    def set_bench_name(self, name):
        self._bench_name = name

    # ---

    def set_device_name(self, name):
        self._device_name = name

    # ---

    def set_tree(self, tree):
        self._tree = tree

    # ---

    def attach_pclient(self, pclient):
        self._pclient = pclient

    # ---

    def initialize(self):
        """Post initialization
        """
        # Keep alive flag
        self.alive = True
        # Flag to know if the topics have been subscribed
        self.__topics_subscribed = False

        # Store attribute representation
        # Contains all the attributes and fields of the driver class in dict
        self.__drv_atts = { }

        # Current state of the driver
        self.__drv_state = 'init'
        self.__drv_state_prev = None

        # # Time where the state started
        # self._state_started_time = 0

        # # Check for name in the driver tree
        # if not ("name" in self._tree):
        #     raise Exception("Name of the interface is required !")

        # Get name
        self._name = self._tree["name"]

        # Init logger
        self.worker_name = f"{self._bench_name}/{self._device_name}/{self._name}"
        self.log = driver_logger(self.worker_name)

        # Check for name in the driver tree
        if not ("info" in self._PZA_DRV_config()):
            raise Exception("Config must have *info* in there *_PZA_DRV_config*")

        # Info attribute
        self.__drv_atts["info"] = self._PZA_DRV_config()["info"]

        # Topic base
        self.topic = "pza/" + self._bench_name + "/" + self._device_name + "/" + self._name
        self.topic_size = len(self.topic)

        # cmds
        self.topic_cmds = self.topic + "/cmds/"
        self.topic_cmds_size = len(self.topic_cmds)

        # atts
        self.topic_atts = self.topic + "/atts/"
        self.topic_atts_size = len(self.topic_atts)
        self.topic_atts_info = self.topic_atts + "info"

        # States
        self.__states = {
            'init': self.__drv_state_init,
            'run': self.__drv_state_run,
            'err': self.__drv_state_err
        }

        # Init event queues
        self._events_pza = queue.Queue()
        self._events_cmds = queue.Queue()

        self.log.info("Interface initialized")

    ###########################################################################
    ###########################################################################

    # def stop(self):
    #     """Request to stop the driver thread
    #     """
    #     # log
    #     self.log.info("Stop requested !")
    #     # Keep alive flag
    #     self.alive = False

    # =============================================================================
    # WORKER FUNCTIONS

    def PZA_WORKER_name(self):
        """
        """
        return self.worker_name

    # ---

    def PZA_WORKER_log(self):
        """
        """
        return self.log

    # ---

    def PZA_WORKER_report(self):
        """Return a stats report of the worker
        """
        report =f"""
    + {self.PZA_WORKER_name()}
        - End state '{self.__drv_state}'
        - Error : {self.__err_string}
        """
        return report

    # ---

    async def PZA_WORKER_task(self, loop):
        """
        """

        try:
            
            # 
            if not self._events_pza.empty():
                event = self._events_pza.get()
                # If the request is for all interfaces '*'
                if event["payload"] == b'*':
                    self.log.info("scan request received !")
                    await self._push_attribute("info", 0, False) # heartbeat_pulse

            if not self._events_cmds.empty():
                event = self._events_cmds.get()
                await self._PZA_DRV_cmds_set(loop, event["payload"])

            # Log state transition
            if self.__drv_state != self.__drv_state_prev:

                # Managed message
                self._state_started_time = time.time()
                self.log.debug(f"STATE CHANGE ::: {self.__drv_state_prev} => {self.__drv_state}")
                self.__drv_state_prev = self.__drv_state

                # Manage the errstring
                if self.__drv_state == "err":
                    self.log.error(f"ERROR !!!")
                    await self._update_attribute("info", "error", self.__err_string, False)
                else:
                    self._remove_attribute_field("info", "error", False)

                # update the state
                await self._update_attribute("info", "state", self.__drv_state)


            # Execute the correct callback
            if not (self.__drv_state in self.__states):
                # error critique !
                pass
            await self.__states[self.__drv_state](loop)

        except Exception as e:
            self._pzadrv_error_detected(str(e) + " " + traceback.format_exc())




    # =============================================================================
    # INTERNAL STATES FUNCTIONS

    # ---

    async def __drv_state_init(self, loop):
        """
        """
        self.__subscribe_topics()
        await self._PZA_DRV_loop_init(loop, self._tree)

    # ---

    async def __drv_state_run(self, loop):
        """
        """
        try:
            await self._PZADRV_loop_run(loop)
        except Exception as e:
            self._pzadrv_error_detected(str(e) + " " + traceback.format_exc())

    # ---

    async def __drv_state_err(self, loop):
        """
        """
        try:
            self.worker_panic()
            await self._PZADRV_loop_err(loop)
        except Exception as e:
            self.log.error(str(e))

    # ---

    # =============================================================================
    # EVENT HANDLERS

    # ---

    def __subscribe_topics(self):
        """Subscribe to the required topics
        """
        if not self.__topics_subscribed:
            # Register the common discovery topic 'pza'
            self._pclient.subscribe("pza", self.__on_pza_message)
            # Register to all commands
            self._pclient.subscribe(self.topic_cmds + "#", self.__on_cmds_message)
            # Valid the flag
            self.__topics_subscribed = True

    def __on_pza_message(self, topic, payload):
        """On scan message callback
        """
        self._events_pza.put({
            "topic":topic, "payload":payload
        })

    def __on_cmds_message(self, topic, payload):
        """On cmds message callback
        """
        self._events_cmds.put({
            "topic":topic, "payload":payload
        })

    ###########################################################################
    ###########################################################################

    async def _update_attribute(self, attribute, field, value, push='on-change', retain = True):
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
            if push == 'on-change' or push == 'always':
                await self._push_attribute(attribute, retain=retain)
            return True

        # Push anyway if the 'push' flag is set to 'always'
        if push == 'always':
            await self._push_attribute(attribute, retain=retain)

        # Attribute not updated
        return False

    # ---

    async def _update_attributes_from_dict(self, change_dict, push=True, retain = True):
        """Function that update multiple attribute and field at the same time
        """
        for attribute in change_dict:
            modification = False
            for field, value in change_dict[attribute].items():
                modification = await self._update_attribute(attribute, field, value, False) or modification
            if push and modification:
                await self._push_attribute(attribute, retain=retain)

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

    async def _push_attribute(self, attribute, qos = 0, retain = True):
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

        # Publish
        await self._pclient.publish_json(topic, pdict, qos=qos, retain=do_retain)

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
    def _PZA_DRV_config(self):
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

    async def _PZA_DRV_loop_init(self, loop, tree):
        """
        """
        self._pzadrv_init_success()

    async def _PZADRV_loop_run(self, loop):
        """
        """
        await asyncio.sleep(0.1)

    async def _PZADRV_loop_err(self, loop):
        """
        """
        elasped = time.time() - self._state_started_time
        if elasped > PlatformDriver.ERROR_TIME_BEFORE_RETRY_S:
            self._pzadrv_restart()
        else:
            await asyncio.sleep(1)
            self.log.debug(f"restart in { int(PlatformDriver.ERROR_TIME_BEFORE_RETRY_S - elasped) }s")

    async def _PZA_DRV_cmds_set(self, loop, payload):
        """Must apply the command on the driver
        """
        pass













    ###########################################################################
    ###########################################################################

    # def hunt(self):
    #     """
    #     """
    #     config = self._PZA_DRV_config()
    #     name = "unnamed" if "name" not in config else config["name"]
    #     description = "" if "description" not in config else config["description"]
    #     template = self._PZADRV_tree_template()
    #     driver = {
    #         "name": name,
    #         "description": description,
    #         "template": template
    #     }
    #     meat = self._PZADRV_hunt_instances()
    #     instances = None
    #     if meat:
    #         instances = {
    #             "name": name,
    #             "instances": meat
    #         }
    #     return driver, instances

