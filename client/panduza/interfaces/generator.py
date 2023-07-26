import time
from ..core.core import Core
from ..core.client import Client
from ..core.interface import Interface

from .dio import Dio
from .bps import Bps
from .ammeter import Ammeter

from .relay import Relay
from .voltmeter import Voltmeter
from ..core.log import create_logger

def GenerateAllInterfacesFromAliases(connections):
    """Generate all the client object from aliases configuration
    """
    __log = create_logger("generator")

    # 
    type_gen = {
        "dio": Dio,
        "bps": Bps,
        "ammeter": Ammeter,
        "relay": Relay,
        "voltmeter": Voltmeter
    }

    # Load aliases
    Core.LoadAliases(connections=connections)

    # Client()
    # broker_alias
    # scan des interfaces pour vérifier

    # Load untyped interfaces first
    interfaces = {}
    for alias in Core.Aliases:
        itf = Interface(alias=alias)
        itf.info.ping()
        interfaces[alias] = itf

    time.sleep(1)

    # Generate interfaces in the correct type
    typed_interfaces = {}
    for name in interfaces:
        __log.info(f"Try to generate interface '{name}'...")
        itf = interfaces[name]
        t = itf.info.get_type()
        __log.info(f"...type found: '{t}' !")
        assert t != "unknown", f"Error > {name} interface does not respond"
        assert t in type_gen, f"Unmanaged interface type {t} by panduza robotF plugin for {name}"
        typed_interfaces[name] = type_gen[t](interface=itf)
        # typed_interfaces[name] = Bps(interface=itf)


    return typed_interfaces



