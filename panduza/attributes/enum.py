import json
from ..attribute import Attribute

class EnumAttribute(Attribute):

    def __init__(self, reactor, topic, mode, settings):
        super().__init__(reactor, topic, mode, settings)

        # Initialize choices if provided in settings
        self.choices = settings.get("choices") if settings else None
        # print("========", settings)

    
    def choices(self):
        """Return the different choices for the attribute."""
        return self.choices
    
    # ---

    def on_att_message(self, data):
        """
        Callback for handling incoming messages.
        - Updates the value and triggers the update event.
        """
        self.value = data.decode()
        self.logger.debug(f"rx {data} => {self.value}")
        super().on_message_top(data)
        
    # ---

    def set(self, value):
        """
        Set the value after converting to the appropriate format.
        - Accepts any type of value: int, float, string, etc.
        - If choices exist, validate the value against the options.
        """
        # Convert non-string values to string
        if not isinstance(value, str):
            converted_value = str(value)
        else:
            converted_value = value  # Keep strings as-is for comparison

        # Optional: Check if the value is in the list of allowed options
        if self.choices and converted_value not in self.choices:
            raise ValueError(
                f"Value '{converted_value}' is not a valid option. "
                f"Allowed choices are: {self.choices}"
            )

        # Convert to JSON format only before sending (if needed)
        mqtt_value = json.dumps(converted_value) if isinstance(value, str) else converted_value

        # Use the parent class's set method to send the value
        super().set(mqtt_value)
        self.logger.debug(f"Set value to {mqtt_value}")
        super().wait_for_value(mqtt_value)
    