import asyncio
import time
from dataclasses import dataclass
from ..core import Interface, Attribute, RoField, RwField  
from asyncio_mqtt import Client, MqttError

@dataclass
class Platform(Interface):
    """Interface to manage power supplies"""

    interface: Interface = None

    def __post_init__(self):

        if self.alias:
            pass
        elif self.interface:
            # Build from another interface
            self.alias = self.interface.alias
            self.addr = self.interface.addr
            self.port = self.interface.port
            self.topic = self.interface.topic
            self.client = self.interface.client

        super().__post_init__()

        # Create MQTT client
        self.mqtt_client = None  # Initialize to None

        # === CONFIG ===
        # Define attributes and fields here
        self.add_attribute(
            Attribute(name_="control")
        ).add_field(
            RwField(name_="running", default=True, description="Always true, set it to false to request the platform stop", type=bool)
        )

        self.add_attribute(
            Attribute(name_="dtree")
        ).add_field(
            RoField(name_="name", type=str, description="name of the active configuration")
        ).add_field(
            RoField(name_="saved", type=bool, description="true if the content is the same as the active config file")
        ).add_field(
            RoField(name_="list", type=list, description="list of all configuration")
        ).add_field(
            RwField(name_="content", description="current tree configuration", type=dict)
        )
        self.add_attribute(
            Attribute(name_="devices")
        ).add_field(
            RoField(name_="hunting", type=bool, default=False, description="true if the platform is currently scanning its ports")
        ).add_field(
            RoField(name_="max", type=int, description="number of device registered")
        ).add_field(
            RoField(name_="hunted", type=int, description="number of device scanned")
        ).add_field(
            RoField(name_="store", type=dict, description="available devices in the platform (including hunt detection)")
        )
        # === PING ATTRIBUTE ===
        self.add_attribute(
            Attribute(name_="ping")
        ).add_field(
            RwField(name_="value", description="Contains the value set by the user", default=0, type=int)
        )


        if self.ensure:
            self.ensure_init()

    async def send_ping_request(self):
        """Send a ping request to the broker."""
        if self.mqtt_client is None:
            raise ValueError("MQTT client not initialized")
        ping_request = {"ping": self.ping.value}  
        await self.send_message_to_broker(ping_request)

    async def send_message_to_broker(self, message):
        """Send message to the broker."""
        if self.mqtt_client is None:
            raise ValueError("MQTT client not initialized")
        await self.mqtt_client.publish(self.topic, str(message))

async def connect_mqtt_client(broker_address="127.0.0.1", broker_port=1883):
    """Connect to the MQTT broker."""
    client = Client(f'mqtt://{broker_address}', port=broker_port, client_id='mqtt-explorer-7cc61f22')
    await client.connect()
    return client

async def send_multiple_pings(platform, num_pings, interval_seconds):
    """Send multiple ping requests with a specified interval."""
    for _ in range(num_pings):
        await platform.send_ping_request()
        await asyncio.sleep(interval_seconds)

async def measure_ping_rate(platform, num_pings, interval_seconds):
    """Measure the ping rate (pings per second)."""
    start_time = time.time()
    await send_multiple_pings(platform, num_pings, interval_seconds)
    end_time = time.time()
    elapsed_time = end_time - start_time
    ping_rate = num_pings / elapsed_time
    return ping_rate

async def main():
    platform = Platform()

    # Connect the MQTT client
    platform.mqtt_client = await connect_mqtt_client()

    num_pings = 500
    interval_seconds = 5

    ping_rate = await measure_ping_rate(platform, num_pings, interval_seconds)
    print(f"Average ping rate: {ping_rate:.2f} pings per second")

    # Disconnect the MQTT client
    await platform.mqtt_client.disconnect()

asyncio.run(main())




