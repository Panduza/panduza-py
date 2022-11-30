"""Example script to configure a power supply through an API_PSU

This example is compatible with the tree **acceptance/features/rsc/psu_tree.json**

"""

# Simple Standalone Test
import sys
import argparse
import time 
from panduza import Core
from panduza import Psu

# Load Aliases
# **acceptance/features/rsc/psu_alias.json**
Core.LoadAliases({
    "local_test": {
        "url": "localhost",
        "port": 1883,
        "interfaces": {
            "Pikachu": "pza/test/hm310t/power"
        }
    }
})

# Create interface
psu = Psu(alias="Pikachu")

# Set voltage


psu.volts.set(5)
time.sleep(3)
psu.volts.set(1)
time.sleep(3)


psu.state.set(True)
time.sleep(3)
psu.state.set(False)
time.sleep(3)
psu.state.set(True, ensure=True)
time.sleep(3)
psu.state.set(False, ensure=True)
