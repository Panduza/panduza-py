import json

from ..attribute import Attribute


class StringAttribute(Attribute):

    def __init__(self, reactor, topic, mode, settings):
        super().__init__(reactor, topic, mode, settings)

    
    # ---

    def on_att_message(self, data):
        """
        Callback for handling incoming messages.
        - Updates the value and triggers the update event.
        """
        self.value = json.loads(data.decode())
        # self.logger.debug(f"rx {data} => {self.value}")
        super().on_message_top(data)
      
      

    def set(self, value):
        # Mode check
        if self.mode == "RO":
            raise Exception("Cannot 'set' a Read-Only attribute")
        
        # Validate the value is a string
        if not isinstance(value, str):
            raise ValueError(f"Value must be a string, got: {type(value)}")
        
        # Encapsulate the string value in JSON format
        string_value = json.dumps(value)
        
        # Use the parent class to send the value
        super().set(string_value)
        # print(f"String value set to {string_value}")