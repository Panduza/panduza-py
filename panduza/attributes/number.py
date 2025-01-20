from ..attribute import Attribute

class NumberAttribute(Attribute):

    def __init__(self, reactor, topic, mode, settings):
        """
        Initialize the NumberAttribute.
        - reactor: the parent reactor handling the attribute.
        - topic: the topic associated with this attribute.
        - mode: read/write mode for the attribute.
        - settings: dictionary containing metadata (min, max, etc.).
        """
        super().__init__(reactor, topic, mode, settings)
        
        # 
        self.user_callback = None

    # ---

    def on_att_message(self, data):
        """
        Callback for handling incoming messages.
        - Updates the value and triggers the update event.
        """
        self.logger.debug(f"rx {data}")
        self.value = float(data)
        super().on_message_top(data)
        if self.user_callback:
            self.user_callback(self.value)

    # ---

    def set_user_callback(self, cb):
        self.user_callback = cb

    # ---
  
    def set(self, value):
        """
        Set a value to the attribute after validation.
        - Ensures the value is a number.
        """
        # Mode check
        if self.mode == "RO":
            raise Exception("Cannot 'set' a Read-Only attribute")
    
        # Validate the value
        if not isinstance(value, int):
            raise ValueError(f"Value must be a number, got: {type(value)}")

        # Set the value using the parent class's method
        super().set(value)
        print(f"NumberAttribute: Set value to {value}")
