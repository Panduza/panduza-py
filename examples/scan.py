import logging
from panduza import Core, Client

logging.basicConfig(level=logging.DEBUG)

Core.LoadAliases({
    "local": {
        "url": "localhost",
        "port": 1883,
        "interfaces": {}
    }
})

client = Client(broker_alias="local")
client.connect()
interfaces = client.scan_interfaces()

print(f"interfaces => {interfaces}")

