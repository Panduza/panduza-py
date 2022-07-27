import json
import logging
from ..core import Interface

class File(Interface):

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
        pass
    
        # file.content.set_from_file()
    
        # self.value     = Attribute_JSON(
        #     client          = self.client,
        #     base_topic      = self.base_topic,
        #     name            = "value",

        #     payload_factory = lambda v: json.dumps({"value": int(v)}).encode("utf-8"),
        #     payload_parser  = lambda v: bool(json.loads(v.decode("utf-8"))["value"])
        # )

        # self.direction = Attribute_JSON(
        #     client          = self.client,
        #     base_topic      = self.base_topic,
        #     name            = "direction",

        #     payload_factory = lambda v: json.dumps({"direction": v}).encode("utf-8"),
        #     payload_parser  = lambda v: json.loads(v.decode("utf-8"))["direction"]
        # )

