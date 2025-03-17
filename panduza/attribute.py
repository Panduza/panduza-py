import logging
import threading
import numpy

class Attribute:
        
    # ---

    def __init__(self, reactor, topic, mode, settings):
        # Create a logger
        self.logger = logging.getLogger(topic)

        self.value = None
        self.client = reactor.client

        self.mode = mode
        self.settings = settings

        self.topic = topic
        self.topic_att = f"{topic}/att"
        self.topic_cmd = f"{topic}/cmd"
        
        self.client.subscribe(self.topic_att)

        # Retry count for waiting for the value
        self.wait_retry = 0

        # Create a thread event for updating the value
        self._update_event = threading.Event()
    
    # ---

    def on_message_top(self, data):
        """ Callback for handling incoming messages. """
        self._update_event.set()
    
    # ---

    def wait_for_first_value(self):
        if isinstance(self.value, numpy.ndarray):
            pass
        else:
            if self.value == None:
                self._update_event.wait(2)
                self._update_event.clear()

    # ---

    def wait_next_value(self, timeout):
        self._update_event.wait(timeout)
        self._update_event.clear()

    # ---

    def wait_for_value(self, value):
        self.wait_retry = 0
        while self.value != value:
            self.logger.debug(f"waiting for value {value}, but current value is {self.value}")
            self._update_event.wait(5)
            self._update_event.clear()

            # Check if the value is still not updated
            self.wait_retry += 1
            if self.wait_retry > 3:
                raise TimeoutError(f"Timeout waiting for value {value}")

    # ---

    def get(self):
        self.wait_for_first_value()
        return self.value
    
    # ---

    def set(self, value):
        self._update_event.clear()
        self.client.publish(self.topic_cmd, value, qos=0)


