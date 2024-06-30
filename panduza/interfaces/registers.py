from dataclasses import dataclass
from ..core import Interface, AttributeA2, AttributeA3, RoField, RwField
import json
import threading

@dataclass
class Registers(Interface):
    """
    """

    interface:Interface = None

    def __post_init__(self):

        self._update_event = threading.Event()
        self._update_event.clear()

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
            AttributeA2( name_ = "commands" )
        )
        self.add_attribute(
            AttributeA3( name_ = "map" )
        )

        self.map.attach_event_listener(self.on_map_update)

    def on_map_update(self, value):
        """
        """
        # print("Map updated")
        self._update_event.set()


    def write(self, index, values):
        """
        """
        json_cmd = {
            "cmd": "w",
            "index": index,
            "values": values
        }
        self.commands.push(json.dumps(json_cmd).encode("utf-8"))

    def read(self, index, size, repeat=None):
        """
        """
        json_cmd = {
            "cmd": "r",
            "index": index,
            "size": size
        }

        if repeat:
            json_cmd["repeat"] = repeat

        self.commands.push(json.dumps(json_cmd).encode("utf-8"))
        self._update_event.wait()

        payload_dict = json.loads(self.map.get().decode("utf-8"))
        # print(payload_dict)
        # print(payload_dict["values"][index:index + size])

        return payload_dict["values"][index:index + size]


