import logging
from panduza import Core, Client


def scan(args):
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

    for iface in interfaces:
        print(f"[{str(interfaces[iface]['type']).rjust(10)}] - {iface}")


