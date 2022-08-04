import json
import magic
import base64
import logging
import threading

from dataclasses import dataclass, field

from ..core import Interface, Attribute, EnsureError


# -----------------------------------------------------------------------------

@dataclass
class MetaDataAttribute(Attribute):
    """
    """
    
    def __init__(self, b_topic, pza_client):
        """Constructor
        """
        super().__init__(client=pza_client, base_topic=b_topic, name='metadata')


    def __post_init__(self):
        """
        """
        super().__post_init__()

        # Subscribe to topic
        self.client.subscribe(self._topic_atts_get, callback=self.__update)


    def __update(self, topic, payload):
        self.__log.debug("Received new value")

        if payload is None:
            self.__data = None
        else:
            self.__data = self.payload_parser(payload)


# -----------------------------------------------------------------------------


@dataclass
class FileContentAttribute(Attribute):
    """
    """
    __data: any = None
    __mime: any = None

    
    def __init__(self, b_topic, pza_client):
        """Constructor
        """
        super().__init__(client=pza_client, base_topic=b_topic, name='content')
        self.__trigger = threading.Event()


    def __post_init__(self):
        """
        """
        super().__post_init__()

        # Subscribe to topic
        self.client.subscribe(self._topic_atts_get, callback=self.__update)


    def __update(self, topic, payload):
        """Callback triggered on reception of an mqtt messsage for this attribute
        """
        self._log.debug("Received new content")

        if payload is None:
            self.__data = None
            self.__mime = None
        else:
            self.__data = json.loads(payload.decode("utf-8"))["data"]
            self._log.debug(f"data : {self.__data}")
            self.__mime = json.loads(payload.decode("utf-8"))["mime"]
            self._log.debug(f"mime : {self.__mime}")
            self.__trigger.set()

        
    def get_data(self):
        """Simple getter for data
        """
        return self.__data


    def get_mime(self):
        """Simple getter for mime
        """
        return self.__mime


    # ---------------------------------
    # Trigger control
    #

    
    def trigger_arm(self):
        self.__trigger.clear()


    def trigger_wait(self, timeout=5):
        try:
            self.__trigger.wait(timeout=timeout)
        except:
            pass
            # raise RuntimeError(f"Error setting timeout {timeout}s trigger wait for attribute {self.name} on {self.base_topic}")


    # ---------------------------------
    # Setters
    #
    

    def set_from_file(self, filepath, mimetype=None, ensure=False):
        """Set the attribute with the content of the file
        """
        # Find the mimettype from the file extension if not overided by the user
        if mimetype == None:
            mimetype = magic.from_file(filepath, mime=True)

        # 
        encoded = base64.b64encode(open(filepath, "rb").read()).decode('ascii')
        
        v = {
            'data': encoded, 'mime': mimetype
        }

        retry=3
        if ensure:
            self.trigger_arm()
        
        self.client.publish(self._topic_cmds_set, self.payload_factory(v))

        if ensure:
            # It is possible that you catch some initialization message with the previous dir value
            # To manage this case, just wait for the correct value
            while self.__data != encoded and retry:
                self._log.debug(f'trigger_wait ! retry={retry}')
                self.trigger_wait(timeout=3)
                if self.__data != encoded:
                    self.trigger_arm()
                    retry-=1

            if self.__data != encoded != v:
                raise EnsureError(f"Attribute {self.name} for {self.base_topic}: cannot set to '{encoded}', got '{self.__data}'")



        
# -----------------------------------------------------------------------------

class File(Interface):
    """Client to manage an File interface
    """


    def __init__(self, alias=None, url=None, port=None, b_topic=None, pza_client=None):
        """Constructor
        """
        super().__init__(alias, url, port, b_topic, pza_client)


    def _post_initialization(self):
        """Initialize attributes
        """    
        self.content = FileContentAttribute(self.base_topic, self.client)
        self.metadata = MetaDataAttribute(self.base_topic, self.client)


