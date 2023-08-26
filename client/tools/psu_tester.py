"""Script to test bpc on the given broker

WARNING : !!! Make sur your Power Supply are not connected to any board !!!
"""
# Import
import sys
import time 
import logging
import argparse
from panduza import Core, Client, Bpc

# Main Variables
BROKER_ADDR="localhost"
BROKER_PORT=1883
CHECK_USER_INPUT=True
RUN_TEST=False
# IFACE_MAX=10000
# logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


def step_set_state(bpc, state, wait_s=3):
    """Step to set the state
    """
    print(f"- set state to {state}")
    bpc.state.value.set(state)
    if CHECK_USER_INPUT:
        in_data = input("Ok or Ko ? [O/k] ")
    else:  
        time.sleep(wait_s)



def step_set_volts(bpc, value, wait_s=3):
    """Step to set the voltage
    """
    print(f"- set volts to {value}")
    bpc.volts.value.set(value)
    if CHECK_USER_INPUT:
        in_data = input("Ok or Ko ? [O/k] ")
    else:  
        time.sleep(wait_s)



def step_set_amps(bpc, value, wait_s=3):
    """Step to set the amps
    """
    print(f"- set amps to {value}")
    bpc.amps.value.set(value)
    if CHECK_USER_INPUT:
        in_data = input("Ok or Ko ? [O/k] ")
    else:  
        time.sleep(wait_s)



def run_test_on_interface(client, topic):
    """Test 1 power supply
    """
    print(f"### Test : ({topic}) ###")

    # Create interface
    bpc = Bpc(topic=topic, client=client)

    # ===
    step_set_volts(bpc, 5)
    step_set_volts(bpc, 10)
    step_set_volts(bpc, 3.3)

    # ===
    step_set_amps(bpc, 0.5)
    step_set_amps(bpc, 3)

    # ===
    step_set_state(bpc, "on")
    step_set_state(bpc, "off")



if __name__ == '__main__':
    """Main entry point
    """
    # Arguments
    parser = argparse.ArgumentParser(
                        prog = 'Pza Power Supply Tester',
                        description = 'Perform test configuration on BPC connected to the broker')
    parser.add_argument('-a', '--broker-address')
    parser.add_argument('-p', '--broker-port')
    # parser.add_argument('-m', '--max')
    parser.add_argument('-y', '--yes', action='store_true')
    args = parser.parse_args()
    if args.broker_address:
        BROKER_ADDR = args.broker_address
    if args.broker_port:
        BROKER_ADDR = args.broker_port
    if args.yes:
        CHECK_USER_INPUT = not args.yes
    # print(args)

    # Check user input
    if not CHECK_USER_INPUT:
        print("Warnings off !")
        RUN_TEST=True
    if not RUN_TEST:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("! Warning be sure your Power Supplies are disconned from any board !")
        print("! This script will set random voltage and trigger all the power    !")
        print("! supplies connected to the given broker                           !")
        print(f">>>>> MQTT Broker : {BROKER_ADDR}:{BROKER_PORT} ")
        in_data = input("Continue ? [y/N] ")
        if in_data == 'y':
            RUN_TEST=True

    # Exit if the test is not authorized to run
    if not RUN_TEST:
        print("Abort !")
        exit(1)

    # Connect the client
    client = Client(url=BROKER_ADDR, port=BROKER_PORT)
    client.connect()

    # Scan interfaces
    print("Scanning...")
    interfaces = client.scan_interfaces()
    for iface in interfaces:
        iface_type = interfaces[iface]["type"]
        if iface_type == "bpc":
            iface_state = interfaces[iface]["state"]
            if iface_state == "run":
                run_test_on_interface(client, iface)
            else:
                print(f"### NOT READY : ({iface}) ###")
                print(f"- in state '{iface_state}'")
                if iface_state == "err":
                    print(f"- ERROR > {interfaces[iface]['error']}")

