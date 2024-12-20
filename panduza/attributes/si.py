from ..attribute import Attribute


class SiAttribute(Attribute):

    def __init__(self, reactor, topic, mode, settings):
        """
        Initialize the NumberAttribute.
        - reactor: the parent reactor handling the attribute.
        - topic: the topic associated with this attribute.
        - mode: read/write mode for the attribute.
        - settings: dictionary containing metadata (min, max, etc.).
        """
        super().__init__(reactor, topic, mode, settings)

        # Initialize properties from settings
        # self._min = settings.get("min", 0)  # Default to 0
        # self._max = settings.get("max", float("inf"))   # Default to no upper limit
        # self.decimals = settings.get("decimals", None)  # For rounding
        # self.unit = settings.get("unit", None)


        self.unit = settings.get("unit")
        self._min = settings.get("min")
        self._max = settings.get("max")
        self.decimals = settings.get("decimals")

        print("========", settings)
        print("========", type(settings))

    def min(self):
        """Return the minimum allowable value for the attribute."""
        return self._min

    def max(self):
        """Return the maximum allowable value for the attribute."""
        return self._max
    
    def decimals(self):
        """Return the decimals allowable for the attribute."""
        return self.decimals
    
    def unit(self):
        """Return the unit of the attribute."""
        return self.unit


    def set(self, value):
        """
        Set a value to the attribute after validation.
        - Ensures the value is a number and within the allowed range.
        """

        # Validate the value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Value must be a number, got: {type(value)}")

        if value < self._min or value > self._max:
            raise ValueError(f"Value {value} is out of bounds! Must be between {self._min} and {self._max}.")
        
        # If decimals are specified, round the value
        if self.decimals is not None:
            value = round(value, self.decimals)

        super().set(value)
        print(f"SiAttribute: Set value to {value}")
