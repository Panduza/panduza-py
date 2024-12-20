import time
import logging
from dataclasses import dataclass, field

from .field import RoField, RwField
from .attribute import Attribute
from .helper import payload_to_dict


@dataclass
class AttributeInfo(Attribute):

    name_: str = "info"
    retain: bool = False

    def __post_init__(self):
        super().__post_init__()
        self.add_field(
            RoField(
                name_ = "type"
            )
        )
        self.add_field(
            RoField(
                name_ = "state"
            )
        )

    def ping(self):
        # TODO just ping the given interface
        self.interface.client.publish("pza", b"*")

    def get_type(self):
        return self._field_data.get("type", "unknown")

    def get_state(self):
        return self._field_data.get("state", "unknown")


