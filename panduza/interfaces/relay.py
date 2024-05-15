from dataclasses import dataclass
from ..core import Interface, Attribute, RwField

@dataclass
class Relay(Interface):
    """Interface to manage relay, two states on/off
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
            Attribute( name_ = "state" )
        ).add_field(
            # true or false
            RwField( name_ = "open" )
        )


        if self.ensure:
            self.ensure_init()

    # open_state: boolean
    def get_state_open(self, open_state):
        return self.state.open.get(open_state)
   
    def set_state_open(self):
        self.state.open.set("constant_power")