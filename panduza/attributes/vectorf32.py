from ..attribute import Attribute

class VectorF32Attribute(Attribute):
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

    def set(self, value):
        """
        Set a boolean value.
        - Ensures the value is either True or False.
        - Sends the boolean value directly (or as a string if required).
        """
        # Mode check
        if self.mode == "RO":
            raise Exception("Cannot 'set' a Read-Only attribute")
        
        # Validate that the input is a boolean
        if not isinstance(value, bool):
            raise ValueError(f"Invalid value for BooleanAttribute. Expected a boolean, got: {type(value)}")

        # Convert boolean to its string equivalent 'true' or 'false' if necessary
        boolean_value = "true" if value else "false"

        # Use the parent class's set method to send the raw value
        super().set(boolean_value)
        self.logger.debug(f"Set value to {boolean_value}")
        
        # Make sur change is ok
        if self.mode == "RW":
            super().wait_for_value(value)
    
