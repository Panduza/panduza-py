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


class PlatformClient(PlatformWorker):
    """
    """

    def __init__(self, addr, port) -> None:
        super().__init__()

        # 
        self.__log = client_logger(str(addr) + ":" + str(port))

        # Initialize state
        # - init
        # 
        self.__state = "init"

        # Mqtt connection
        self.mqtt_client = mqtt.Client()
        # self.mqtt_client.on_message = self.__on_message


    # ---

    async def _PZA_WORKER_task(self):
        """
        """
        
        self.__log.info("poooo")
        # time.sleep(0.5)
        # asyncio.sleep()

    # ---

