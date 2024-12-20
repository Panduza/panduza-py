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

    

    def set(self, value):
        """
        Set a value to the attribute after validation.
        - Ensures the value is a number.
        """
        # Validate the value
        if not isinstance(value, int):
            raise ValueError(f"Value must be a number, got: {type(value)}")

        # Set the value using the parent class's method
        super().set(value)
        print(f"NumberAttribute: Set value to {value}")
