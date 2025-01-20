import json
from ..attribute import Attribute


class MemoryCommandAttribute(Attribute):
    """
    """

    # ---

    def __init__(self, reactor, topic, mode, settings=None):
        super().__init__(reactor, topic, mode, settings)

    # ---

    def on_att_message(self, data):
        """
        Callback for handling incoming messages.
        - Updates the value and triggers the update event.
        """
        self.logger.debug(f"rx {data}")
        if data == b"true":
            self.value = True
        elif data == b"false":
            self.value = False
        else:
            print("Invalid boolean value received:", data)
        super().on_message_top(data)
    
    # ---

    def set_read_command(self, address, size):
        """
        """
        # Mode check
        if self.mode == "RO":
            raise Exception("Cannot 'set' a Read-Only attribute")
        
        # 
        payload = {
            "mode": "Read",
            "address": address,
            "size": size,
        }
        
        # 
        try:
            # Serialize the value to JSON
            json_value = json.dumps(payload)

            # Use the parent class's set method to send the value
            super().set(json_value)
            print(f"JSON value set to: {json_value}")

        except (TypeError, ValueError) as e:
            # Raise an error if the value cannot be serialized to JSON
            raise ValueError(f"Invalid JSON value: {payload}. Error: {str(e)}")


    # ---

    def set_write_command(self, address, values):
        """
        """
        # Mode check
        if self.mode == "RO":
            raise Exception("Cannot 'set' a Read-Only attribute")

        # 
        values_data = []
        if isinstance(values, int):
            values_data.append(values)
        elif isinstance(values, list):
            values_data = values
        else:
            raise Exception(f"Unsupported type {type(values)}")

        # 
        payload = {
            "mode": "Write",
            "address": address,
            "values": values_data,
        }

        # 
        try:
            # Serialize the value to JSON
            json_value = json.dumps(payload)

            # Use the parent class's set method to send the value
            super().set(json_value)
            print(f"JSON value set to: {json_value}")

        except (TypeError, ValueError) as e:
            # Raise an error if the value cannot be serialized to JSON
            raise ValueError(f"Invalid JSON value: {payload}. Error: {str(e)}")

    