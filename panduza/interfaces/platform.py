import asyncio
import time
from dataclasses import dataclass
import paho.mqtt.client as mqtt
from core import Interface


@dataclass
class Platform:
    """Interface to manage power supplies"""

    interface: Interface = None

    def __post_init__(self):
        
        if self.interface:
            # Build from another interface
            self.topic = self.interface.topic
            self.client = self.interface.client
        else:
            # Default topic if no interface is provided
            self.topic = "power_supply/status"
            self.client = None

        # Create MQTT client (initialized to None)
        self.mqtt_client = None

    def on_connect(self, client, userdata, flags, rc):
        """Callback function called when an MQTT connection is established."""
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg):
        """Callback function called when a message is received."""
        print(msg.topic+" "+str(msg.payload))

    async def send_ping_request(self):
        """Sends a ping request to the MQTT broker."""
        if self.mqtt_client is None:
            raise ValueError("MQTT client not initialized")
        ping_request = {"ping": 1}  # Example ping message
        await self.send_message_to_broker(ping_request)

    async def send_message_to_broker(self, message):
        """Sends a message to the MQTT broker."""
        if self.mqtt_client is None:
            raise ValueError("MQTT client not initialized")
        self.mqtt_client.publish(self.topic, str(message))

async def connect_mqtt_client(broker_address="localhost", broker_port=1883):
    """Connects to the MQTT broker."""
    client = mqtt.Client(client_id='mqtt-explorer-7cc61f22')
    client.on_connect = on_connect
    client.connect(broker_address, broker_port, 60)
    return client

async def send_multiple_pings(platform, num_pings, interval_seconds):
    """Sends multiple ping requests with a specified interval."""
    for _ in range(num_pings):
        await platform.send_ping_request()
        await asyncio.sleep(interval_seconds)

async def measure_ping_rate(platform, num_pings, interval_seconds):
    """Measures the ping rate (pings per second)."""
    start_time = time.time()
    await send_multiple_pings(platform, num_pings, interval_seconds)
    end_time = time.time()
    elapsed_time = end_time - start_time
    ping_rate = num_pings / elapsed_time
    return ping_rate

async def main():
    # Connect to the MQTT client
    mqtt_client = await connect_mqtt_client()

    # Create the platform with a default interface
    platform = Platform()

    # Assign MQTT client to the platform
    platform.mqtt_client = mqtt_client

    # Number of pings and interval between each ping
    num_pings = 500
    interval_seconds = 5

    # Measure ping rate
    ping_rate = await measure_ping_rate(platform, num_pings, interval_seconds)
    print(f"Average ping rate: {ping_rate:.2f} pings per second")

    # Disconnect MQTT client
    await platform.mqtt_client.disconnect()

# Execute the main program
asyncio.run(main())



