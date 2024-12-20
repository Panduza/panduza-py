import logging
import threading


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
        
        # Create a thread event for updating the value
        self._update_event = threading.Event()
    
    # ---

    def on_message_top(self, data):
        """ Callback for handling incoming messages. """
        self._update_event.set()
    
    # ---

    def wait_for_first_value(self):
        if self.value == None:
            self._update_event.wait(1)
    
    # ---

    def wait_for_value(self, value):
        while self.value != value:
            self.logger.debug(f"waiting for value {value} current value {self.value}")
            self._update_event.wait(5)
            self._update_event.clear()
    
    # ---

    def get(self):
        return self.value
    
    # ---

    def set(self, value):
        self._update_event.clear()
        self.client.publish(self.topic_cmd, value, qos=0)


