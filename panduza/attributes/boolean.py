from ..attribute import Attribute

class BooleanAttribute(Attribute):
    """
    Attribute for sending boolean values (True or False).
    Ensures that only valid booleans are sent.
    """

    def __init__(self, reactor, topic, mode, settings=None):
        super().__init__(reactor, topic, mode, settings)

    def set(self, value):
        """
        Set a boolean value.
        - Ensures the value is either True or False.
        - Sends the boolean value directly (or as a string if required).
        """
        # Validate that the input is a boolean
        if not isinstance(value, bool):
            raise ValueError(f"Invalid value for BooleanAttribute. Expected a boolean, got: {type(value)}")

        # Convert boolean to its string equivalent 'true' or 'false' if necessary
        boolean_value = "true" if value else "false"

        # Use the parent class's set method to send the raw value
        super().set(boolean_value)
        print(f"Boolean value set to: {boolean_value}")
