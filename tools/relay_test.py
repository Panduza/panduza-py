import time
import argparse

from panduza import Relay, Client

# Main Variables
BROKER_ADDR="localhost"
BROKER_PORT=1883

def channel_set_state(relay, state, wait_s=3):
    """Step to set the state
    """
    print(f"- set state to {state}")
    relay.state.open.set(state)

# ---
        
def run_test_on_interface(client, topic):
    """Test voxpower inhibiter
    """
    print(f"### Test : ({topic}) ###")

    # Create interface
    relay = Relay(topic=topic, client=client)

    # ===
    channel_set_state(relay, True)
    time.sleep(1)
    channel_set_state(relay, False)
    time.sleep(0.5)

# ---

if __name__ == '__main__':
    """Main entry point
    """
    # Arguments
    parser = argparse.ArgumentParser(
                        prog = 'Pza Voxower Inhibiter Tester',
                        description = 'Perform test configuration on BPC connected to the broker')
    parser.add_argument('-a', '--broker-address')
    parser.add_argument('-p', '--broker-port')
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
    interfaces = client.scan_all_interfaces(1)
    print(interfaces)
    for iface in interfaces:
        iface_type = interfaces[iface]["type"]
        if iface_type == "relay":
            iface_state = interfaces[iface]["state"]
            if iface_state == "run":# and iface == "pza/default/test/channel_2:_ctrl":
                run_test_on_interface(client, iface)
            else:
                print(f"### NOT READY : ({iface}) ###")
                print(f"- in state '{iface_state}'")
                if iface_state == "err":
                    print(f"- ERROR > {interfaces[iface]['error']}")