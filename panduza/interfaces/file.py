import json
import base64
import logging

from dataclasses import dataclass, field

from ..core import Interface, Attribute



@dataclass
class FileContentAttribute(Attribute):
    """
    """
    
    def __init__(self, client):
        """Constructor
        """
        self.name = 'content'
        self.client = client
    

    def set_from_file(self, filepath, mimetype="text/plain"):
        """Set the attribute with the content of the file
        """
        
        encoded = base64.b64encode(open(filepath, "rb").read()).decode('ascii')
        
        v = {
            'content': encoded, 'mime': mimetype
        }
        
        self.client.publish(self._topic_cmds_set, self.payload_factory(v))
        


class File(Interface):
    """
    """
    
    ###########################################################################
    ###########################################################################
    
    def __init__(self, alias=None, url=None, port=None, b_topic=None, pza_client=None):
        """Constructor
        """
        super().__init__(alias, url, port, b_topic, pza_client)

    ###########################################################################
    ###########################################################################

    def _post_initialization(self):
        """Initialize attributes
        """
    
        self.content = FileContentAttribute(self.client)


