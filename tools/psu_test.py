"""Script to test psu on the given broker

WARNING : !!! Make sur your Power Supply are not connected to any board !!!
"""
# Import
import sys
import time 
import argparse
from panduza import Core, Client, Psu

# Main Variables
BROKER_ADDR="localhost"
BROKER_PORT=1883
CHECK_USER_INPUT=True
RUN_TEST=False



def step_set_state(psu, state, wait_s=3):
    """Step to set the state
    """
    print(f"- set state to {state}")
    psu.state.set(state)
    if CHECK_USER_INPUT:
        in_data = input("Ok or Ko ? [O/k]")
    else:  
        time.sleep(wait_s)



def step_set_volts(psu, value, wait_s=3):
    """Step to set the voltage
    """
    print(f"- set volts to {value}")
    psu.volts.set(value)
    if CHECK_USER_INPUT:
        in_data = input("Ok or Ko ? [O/k]")
    else:  
        time.sleep(wait_s)



def step_set_amps(psu, value, wait_s=3):
    """Step to set the amps
    """
    print(f"- set amps to {value}")
    psu.amps.set(value)
    if CHECK_USER_INPUT:
        in_data = input("Ok or Ko ? [O/k]")
    else:  
        time.sleep(wait_s)



def run_test_on_interface(client, b_topic):
    """Test 1 power supply
    """
    print(f"### Test : ({b_topic}) ###")

    # Create interface
    psu = Psu(b_topic=b_topic, pza_client=client)

    # ===
    step_set_volts(psu, 5)
    step_set_volts(psu, 10)
    step_set_volts(psu, 3.3)

    # ===
    step_set_amps(psu, 0.5)
    step_set_amps(psu, 3)

    # ===
    step_set_state(psu, True)
    step_set_state(psu, False)



if __name__ == '__main__':
    """Main entry point
    """
    # Arguments
    parser = argparse.ArgumentParser(
                        prog = 'Pza Power Supply Tester',
                        description = 'Perform test configuration on PSU connected to the broker')
    parser.add_argument('-a', '--broker-address')
    parser.add_argument('-p', '--broker-port')
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
        in_data = input("Continue ? [y/N]")
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
        if iface_type == "psu":
            run_test_on_interface(client, iface)




    # # Load Aliases
    # # **acceptance/features/rsc/psu_alias.json**
    # Core.LoadAliases({
    #     "local_test": {
    #         "url": "localhost",
    #         "port": 1883,
    #         "interfaces": {
    #             "Pikachu": "pza/test/hm310t/power"
    #         }
    #     }
    # })


    # # Set voltage





    # psu.state.set(True)
    # time.sleep(3)
    # psu.state.set(False)
    # time.sleep(3)
    # psu.state.set(True, ensure=True)
    # time.sleep(3)
    # psu.state.set(False, ensure=True)
