import json
import base64
import threading
from dataclasses import dataclass, field
from ..core import Interface
from ..core import Interface, Attribute, EnsureError, RoField, RwField



@dataclass
class AttributeData(Attribute):
    _rx_buffer: bytes = b''


    def _on_att_message(self, topic, payload):
        self._log.debug("overload !!!")

        payload_dict = json.loads(payload.decode("utf-8"))
        self._log.debug(f"{payload_dict}")

        if 'rx' in payload_dict['data']:
            rx_string = payload_dict['data']['rx']
            base64_bytes = rx_string.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)

            self._rx_buffer += message_bytes
        
            self._log.debug(f"{self._rx_buffer}")


    def read(self, size = None):
        data = self._rx_buffer[:size]
        self._rx_buffer = self._rx_buffer[len(data):]
        return data



class Serial(Interface):
    """Interface to manage power supplies
    """

    # ---

    def __init__(self, alias=None, addr=None, port=None, topic=None, client=None):
        """! Constructor
        """
        super().__init__(alias, addr, port, topic, client)

    # ---

    def _post_initialization(self):
        """! Declare attributes here
        """
        # === STATE ===
        self.add_attribute(
            AttributeData(
                name = "data"
            )
        ).add_field(
            RwField(
                name = "tx"
            )
        ).add_field(
            RwField(
                name = "rx"
            )
        )

    # ---

    def write(self, tx_data: bytes):
        tx_encoded = base64.b64encode(tx_data)
        base64_message = tx_encoded.decode('ascii')
        self.data.tx.set(base64_message)

    # ---

    def read(self, size = None):
        return self.data.read(size)


