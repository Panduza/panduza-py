"""Script to test bps on the given broker

WARNING : !!! Make sur your Power Supply are not connected to any board !!!
"""
# Import
import os
import sys
import time 
import logging
import argparse
from panduza import Core, Client, ModbusClient

# Main Variables
BROKER_ADDR="localhost"
BROKER_PORT=1883

# logging.basicConfig(encoding='utf-8', level=logging.DEBUG)






def run_terminal_on_interface(client, topic):
    """Test 1 power supply
    """
    print(f"### Start Terminal On : ({topic}) ###")

    # Create interface
    mbc = ModbusClient(topic=topic, client=client)


    
    while True:
        command = input("[w|r] addr [value|size] [unit] > ")
        command_list = command.split()

        cmd = command_list[0]
        add = command_list[1]
        val = command_list[2]
        unt = command_list[3]

        if cmd == "w":
            payload = { unt: { add: val } }
            mbc.holding_regs.values.set(payload)
        elif cmd == "r":
            payload = { "type": "holding_regs", "address": add, "size": val, "unit": unt,"polling_time_s": 1 }
            mbc.watchlist.configs.set(payload)


if __name__ == '__main__':
    """Main entry point
    """
    # Arguments
    parser = argparse.ArgumentParser(
                        prog = 'Pza Simple Modbus Client Terminal',
                        description = 'Provide a simple terminal to perform modbus client R/W operations')
    parser.add_argument('-a', '--broker-address')
    parser.add_argument('-p', '--broker-port')
    # parser.add_argument('-m', '--max')

    args = parser.parse_args()
    if args.broker_address:
        BROKER_ADDR = args.broker_address
    if args.broker_port:
        BROKER_ADDR = args.broker_port

    # Connect the client
    client = Client(url=BROKER_ADDR, port=BROKER_PORT)
    client.connect()

    # Scan interfaces
    print("Scanning...")
    interfaces = client.scan_interfaces()
    for iface in interfaces:
        iface_type = interfaces[iface]["type"]
        if iface_type == "modbus.client":
            iface_state = interfaces[iface]["state"]
            if iface_state == "run":
                run_terminal_on_interface(client, iface)
            else:
                print(f"### NOT READY : ({iface}) ###")
                print(f"- in state '{iface_state}'")
                if iface_state == "err":
                    print(f"- ERROR > {interfaces[iface]['error']}")

