import json
from ..attribute import Attribute

class JsonAttribute(Attribute):
    """
    Attribute for sending JSON-formatted data.
    It validates and serializes Python objects into JSON strings before sending.
    """

    def __init__(self, reactor, topic, mode, settings=None):
        super().__init__(reactor, topic, mode, settings)

    def set(self, value):
        """
        Set a JSON-compatible value.
        - Accepts dictionaries, lists, or any data that can be serialized to JSON.
        - Converts the value to a JSON string before sending it.
        """
        try:
            # Serialize the value to JSON
            json_value = json.dumps(value)

            # Use the parent class's set method to send the value
            super().set(json_value)
            # print(f"JSON value set to: {json_value}")

        except (TypeError, ValueError) as e:
            # Raise an error if the value cannot be serialized to JSON
            raise ValueError(f"Invalid JSON value: {value}. Error: {str(e)}")
