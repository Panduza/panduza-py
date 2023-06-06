from dataclasses import dataclass
from ..core import Interface, Attribute, RoField, RwField

@dataclass
class Psu(Interface):
    """Interface to manage power supplies
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

        # === ENABLE ===
        self.add_attribute(
            Attribute( name = "enable" )
        ).add_field(
            RwField( name = "value" )
        )

        # === VOLTS ===
        self.add_attribute(
            Attribute( name = "volts" )
        ).add_field(
            RoField( name = "real" )
        ).add_field(
            RwField( name = "goal" )
        ).add_field(
            RoField( name = "min" )
        ).add_field(
            RoField( name = "max" )
        ).add_field(
            RoField( name = "decimals" )
        ).add_field(
            RwField( name = "polling_cycle" )
        )

        # === AMPS ===
        self.add_attribute(
            Attribute( name = "amps" )
        ).add_field(
            RoField( name = "real" )
        ).add_field(
            RwField( name = "goal" )
        ).add_field(
            RoField( name = "min" )
        ).add_field(
            RoField( name = "max" )
        ).add_field(
            RoField( name = "decimals" )
        ).add_field(
            RwField( name = "polling_cycle" )
        )

        # === SETTINGS ===
        self.add_attribute(
            Attribute( name = "settings", bypass_init_ensure = True )
        ).add_field(
            RwField( name = "ovp" )
        ).add_field(
            RwField( name = "ocp" )
        ).add_field(
            RwField( name = "silent" )
        )

        # === MISC ===
        self.add_attribute(
            Attribute( name = "misc", bypass_init_ensure = True  )
        )

        if self.ensure:
            self.ensure_init()

