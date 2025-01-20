from ..attribute import Attribute

class SiAttribute(Attribute):
    
    # ---

    def __init__(self, reactor, topic, mode, settings):
        """
        Initialize the NumberAttribute.
        - reactor: the parent reactor handling the attribute.
        - topic: the topic associated with this attribute.
        - mode: read/write mode for the attribute.
        - settings: dictionary containing metadata (min, max, etc.).
        """
        super().__init__(reactor, topic, mode, settings)

        self._unit = settings.get("unit")
        self._min = settings.get("min")
        self._max = settings.get("max")
        self._decimals = settings.get("decimals")
    
    # ---

    def min(self):
        """Return the minimum allowable value for the attribute."""
        return self._min
    
    # ---

    def max(self):
        """Return the maximum allowable value for the attribute."""
        return self._max
        
    # ---

    def decimals(self):
        """Return the decimals allowable for the attribute."""
        return self._decimals
        
    # ---

    def unit(self):
        """Return the unit of the attribute."""
        return self._unit
    
    # ---

    def on_att_message(self, data):
        """
        Callback for handling incoming messages.
        - Updates the value and triggers the update event.
        """
        self.logger.debug(f"rx {data}")
        self.value = float(data)
        super().on_message_top(data)
    
    # ---

    def set(self, value):
        """
        Set a value to the attribute after validation.
        - Ensures the value is a number and within the allowed range.
        """
        # Mode check
        if self.mode == "RO":
            raise Exception("Cannot 'set' a Read-Only attribute")

        # Validate the value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Value must be a number, got: {type(value)}")

        # If decimals are specified, round the value
        if self._decimals is not None:
            value = round(value, self._decimals)

        if value < self._min or value > self._max:
            raise ValueError(f"Value {value} is out of bounds! Must be between {self._min} and {self._max}.")

        super().set(value)
        self.logger.debug(f"Set value to {value}")

        # Make sur change is ok
        if self.mode == "RW":
            super().wait_for_value(value)

