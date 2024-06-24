from dataclasses import dataclass
from ..core import Interface, AttributeA3, RoField, RwField
import json

@dataclass
class Registers(Interface):
    """
    """

    interface:Interface = None

    def __post_init__(self):

        if self.alias:
            pass
        elif self.interface:
            # Build from an other interface
            self.alias = self.interface.alias
            self.addr = self.interface.addr
            self.port = self.interface.port
            self.topic = self.interface.topic
            self.client = self.interface.client

        super().__post_init__()

        # === MEASURE ===
        self.add_attribute(
            AttributeA3( name_ = "commands" )
        )

    def write(self, index, values):
        """
        """
        json_cmd = {
            "cmd": "w",
            "index": index,
            "values": values
        }
        self.commands.push(json.dumps(json_cmd).encode("utf-8"))


