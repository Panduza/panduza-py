from ..attribute import Attribute
from ..fbs import Notification
import time

class NotificationAttribute(Attribute):
    """
    Attribute for sending boolean values (True or False).
    Ensures that only valid booleans are sent.
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
        object = Notification.Notification.GetRootAsVectorF32(data, 0)

        super().on_message_top(object)
    
