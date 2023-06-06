import json
import threading
from ..core import Interface
from ..core import Interface, Attribute, EnsureError, RoField, RwField

class ModbusClient(Interface):
    """Interface to manage power supplies
    """

    # Used when the user want to create a specialized interface from a generic one
    interface:Interface = None

    ###########################################################################
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

        # === HOLDING REGISTERS ===
        self.add_attribute(
            Attribute(
                name = "holding_regs"
            )
        ).add_field(
            RwField(
                name = "values"
            )
        )

        # === WATCHLIST ===
        self.add_attribute(
            Attribute(
                name = "watchlist"
            )
        ).add_field(
            RwField(
                name = "configs"
            )
        )

        # Init the watchlist
        self._watchlist = []

    ###########################################################################
    def watch_holding_regs(self, addr, size, unit, polling_time_s = 2):
        """Append an entry in the watchlist
        """
        # Append the new entry
        self._watchlist.append({
            "type": "holding_regs",
            "address": addr, "size": size, "unit": unit,"polling_time_s": polling_time_s
        })
        # Set the new list
        self.watchlist.configs.set(self._watchlist)

    ###########################################################################
    def clear_watchlist():
        """Clear the watchlist
        """
        self._watchlist = []
        self.watchlist.configs.set(self._watchlist)


