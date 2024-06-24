from dataclasses import dataclass
from ..core import Interface, Attribute, RoField, RwField


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
            Attribute( name_ = "measure" )
        ).add_field(
            RoField( name_ = "value" )
        ).add_field(
            RoField( name_ = "decimals" )
        ).add_field(
            RwField( name_ = "afrq" )
        )

        if self.ensure:
            self.ensure_init()


    

