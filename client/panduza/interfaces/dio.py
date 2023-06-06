from dataclasses import dataclass
from ..core import Interface, Attribute, RwField

@dataclass
class Dio(Interface):
    """Interface to manage DIO
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

        # === DIRECTION ===
        self.add_attribute(
            Attribute( name = "direction" )
        ).add_field(
            RwField( name = "value")
        ).add_field(
            RwField( name = "pull")
        ).add_field(
            RwField( name = "polling_cycle")
        )

        # === STATE ===
        self.add_attribute(
            Attribute( name = "state" )
        ).add_field(
            RwField( name = "active" )
        ).add_field(
            RwField( name = "active_low" )
        ).add_field(
            RwField( name = "polling_cycle" )
        )

        if self.ensure:
            self.ensure_init()
