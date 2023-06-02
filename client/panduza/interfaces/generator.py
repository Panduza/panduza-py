import time
from ..core.core import Core
from ..core.interface import Interface

from .psu import Psu
from ..core.log import create_logger

def GenerateAllInterfacesFromAliases(connections):
    """Generate all the client object from aliases configuration
    """
    __log = create_logger("generator")

    # 
    type_gen = {
        "psu": Psu
    }

    # Load aliases
    Core.LoadAliases(connections=connections)

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
        itf = interfaces[name]
        t = itf.info.get_type()
        __log.info(f"Generate interface '{name}' with type '{t}' !")
        assert t != "unknown", f"Error > {name} interface does not respond"
        typed_interfaces[name] = type_gen[t](interface=itf)
        # typed_interfaces[name] = Psu(interface=itf)


    return typed_interfaces



