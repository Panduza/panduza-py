import json
import magic
import base64
import logging

from dataclasses import dataclass, field

from ..core import Interface, Attribute



@dataclass
class FileContentAttribute(Attribute):
    """
    """
    
    def __init__(self, b_topic, pza_client):
        """Constructor
        """
        super().__init__(client=pza_client, base_topic=b_topic, name='content')

        
    def set_from_file(self, filepath, mimetype=None):
        """Set the attribute with the content of the file
        """
        # Find the mimettype from the file extension if not overided by the user
        if mimetype == None:
            mimetype = magic.from_file(filepath, mime=True)

        # 
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
    
        self.content = FileContentAttribute(self.base_topic, self.client)


