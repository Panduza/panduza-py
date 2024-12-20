import json

from ..attribute import Attribute


class StringAttribute(Attribute):

    def __init__(self, reactor, topic, mode, settings):
        super().__init__(reactor, topic, mode, settings)


    def set(self, value):
        # Validate the value is a string
        if not isinstance(value, str):
            raise ValueError(f"Value must be a string, got: {type(value)}")
        
        # Encapsulate the string value in JSON format
        string_value = json.dumps(value)
        
        # Use the parent class to send the value
        super().set(string_value)
        # print(f"String value set to {string_value}")