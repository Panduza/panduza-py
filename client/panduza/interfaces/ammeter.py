from dataclasses import dataclass
from ..core import Interface, Attribute, RoField, RwField

@dataclass
class Ammeter(Interface):
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
            Attribute( name = "measure" )
        ).add_field(
            RoField( name = "value" )
        ).add_field(
            RwField( name = "polling_cycle" )
        )

        if self.ensure:
            self.ensure_init()

