import os
import json
import pkgutil
import argparse
import threading
import importlib
from sys import platform

from .conf import PLATFORM_VERSION
from .broker import Broker


from .log.platform import platform_logger

from .inbuilt import PZA_DRIVERS_LIST as INBUILT_DRIVERS
from .drivers.std import PZA_DRIVERS_LIST as STD_DRIVERS
from .drivers.fake import PZA_DRIVERS_LIST as FAKE_DRIVERS
from .drivers.ftdi import PZA_DRIVERS_LIST as FTDI_DRIVERS
from .drivers.aardvark import PZA_DRIVERS_LIST as AARDVARK_DRIVERS


class MetaPlatform:
    """ Main class to manage the platform

    **Execution order**

    - __init__
    - parse_args ??deprecated??
    - register_driver_plugin_discovery
    - run
        - __load_tree_broker

    """

    ###########################################################################
    ###########################################################################

    def __init__(self, run_dir="/etc"):
        """ Constructor
        """
        # Init the platform logger
        self._log = platform_logger()
        self.run_dir = run_dir

        # Debug logs to structure log file
        self._log.info("==========================================")
        self._log.info(f"= PANDUZA PYTHON PLATFORM          {PLATFORM_VERSION} =")
        self._log.info("==========================================")

        # Threads
        self.threads = []

        # Drivers
        self.drivers = []

        # Interfaces
        self.interfaces = []

        # Tree that must be loaded at startup
        self.tree_filepath = None

        #
        self.force_log = False

    ###########################################################################
    ###########################################################################

    def load_tree_overide(self, tree_filepath):
        """platform will use the given tree filepath
        """
        self.tree_filepath = tree_filepath
        self._log.debug(f"force tree:{self.tree_filepath}")

    ###########################################################################
    ###########################################################################

    def parse_args(self):
        """
        """
        # Manage arguments
        parser = argparse.ArgumentParser(description='Manage Panduza Platform')
        parser.add_argument('-t', '--tree', help='path to the panduza tree (*.json)', metavar="FILE")
        parser.add_argument('-l', '--log', dest='enable_logs', action='store_true', help='start the logs')
        args = parser.parse_args()

        # Check if logs are enabled
        if not args.enable_logs and self.force_log != True:
            self._log.remove()

        # Check tree filepath value
        self.tree_filepath = args.tree

    ###########################################################################
    ###########################################################################

    def __load_tree_broker(self, machine, broker_name, broker_tree):
        """ Load interfaces declared in the tree for the given broker
        """
        # Debug log
        self._log.info(f" + {broker_name} ({broker_tree['addr']}:{broker_tree['port']})")

        # Create broker object
        broker = Broker(broker_tree["addr"], broker_tree["port"])

        # For each interface create it
        for interface in broker_tree["interfaces"]:
            self.__interpret_interface_declaration(machine, broker, interface)

        # Append the platform interface on each managed broker
        self.__interpret_interface_declaration(machine, broker, {
            "name": "py",
            "group": "platform",
            "driver": "py.platform"
        })

    ###########################################################################
    ###########################################################################

    def __replace_r_with_param(self, element, param):
        """
        """
        # If the element is a dict, replace on each value (not in the keys)
        if isinstance(element, dict):
            new_dict = {}
            for key in element:
                new_dict[key] = self.__replace_r_with_param(element[key], param)
            return new_dict

        # If the element is a string, replace %r with param
        elif isinstance(element, str):
            return element.replace("%r", str(param))


        # TODO
        # if element is arry

    ###########################################################################
    ###########################################################################

    def __interpret_interface_declaration(self, machine, broker, interface_declaration):
        """ Interpret option in the interface declaration

        Options are
        - disabled: to prevent this interface from beeing loaded
        - repeated: to execute the interface loading multiple times
        """
        # Check if the interface is disabled by the user
        if "disabled" in interface_declaration and interface_declaration["disabled"] == True:
            name = "?"
            if "name" in interface_declaration:
                name = interface_declaration["name"]
            driver_name = "?"
            if "driver" in interface_declaration:
                driver_name = interface_declaration["driver"]
            self._log.warning(f"> {name} [{driver_name}] interface disabled")
            return

        # Multiple interfaces, need to create one interface for each
        if "repeated" in interface_declaration:
            for param in interface_declaration["repeated"]:
                formated_interface_info = self.__replace_r_with_param(interface_declaration, param)
                self.__load_interface(machine, broker, formated_interface_info)

        # Only one interface to start
        else:
            self.__load_interface(machine, broker, interface_declaration)

    ###########################################################################
    ###########################################################################

    def __load_interface(self, machine, broker, interface_info):
        """
        """
        name = interface_info["name"]
        driver_name = interface_info["driver"]

        try:
            driver_obj = self.__get_compatible_driver(driver_name)

            instance = driver_obj()
            instance.initialize(self, machine, broker, interface_info)
            self.interfaces.append({
                "name": name,
                "instance":instance
            })

            self._log.info(f"> {name} [{driver_name}]")
        except Exception as e:
            self._log.error(f"{driver_name} : {name} ({str(e)})")

    ###########################################################################
    ###########################################################################

    def __get_compatible_driver(self, driver_name):
        """Walk through driver and try to find a matching one for the given driven name
        """
        for drv in self.drivers:
            # Driver must provide a compatibilty array
            # If the driver name is in the array then it is considered compatible
            compat = drv()._PZADRV_config()["compatible"]
            if isinstance(compat, list):
                if driver_name in compat:
                    return drv
            elif isinstance(compat, str):
                if driver_name == compat:
                    return drv
        raise Exception("driver not found")

    ###########################################################################
    ###########################################################################

    def register_driver_plugin_discovery(self):
        """Function to discover python plugins related to panduza python platform
        """
        #
        # self._log.debug(f"PYPATH: {sys.path}")
        # help('modules')

        # Discovering process
        self._log.debug("Start plugin discovery")
        discovered_plugins = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in pkgutil.iter_modules()
            if name.startswith("panduza_class")
        }
        self._log.debug(f"Discovered plugins: {str(discovered_plugins)}")

        # Import plugin inside the platform manager
        # Each class plugins export a PZA_DRIVERS_LIST with the list of all the managed drivers
        for plugin_name in discovered_plugins :
            self._log.info(f"Load plugin: '{plugin_name}'")
            plugin_package = __import__(plugin_name)
            for drv in plugin_package.PZA_DRIVERS_LIST:
                self.register_driver(drv)

        # Register drivers already packaged with the platform
        for drv in STD_DRIVERS:
            self.register_driver(drv)
        for drv in FAKE_DRIVERS:
            self.register_driver(drv)
        for drv in INBUILT_DRIVERS:
            self.register_driver(drv)
        for drv in FTDI_DRIVERS:
            self.register_driver(drv)
        for drv in AARDVARK_DRIVERS:
            self.register_driver(drv)

    ###########################################################################
    ###########################################################################

    def get_interface_instance_from_name(self, name):
        """
        """
        for interface in self.interfaces:
            if interface["name"] == name:
                return interface["instance"]
        raise Exception("interface not found")

    ###########################################################################
    ###########################################################################

    def register_driver(self, driver):
        """
        """
        self._log.info(f"Register driver: {driver()._PZADRV_config()['compatible']}")
        self.drivers.append(driver)

    ###########################################################################
    ###########################################################################

    def hunt_mode(self):
        """Fonction to perform the interface auto-detection on the system
        """
        self._log.info("*********************************")
        self._log.info("*** !!! HUNT MODE ENABLED !!! ***")
        self._log.info("*********************************")

        os.makedirs(f"{self.run_dir}/panduza/platform", exist_ok=True)
        filepath = f"{self.run_dir}/panduza/platform/py.json"

        f = open(filepath, "w")

        hunting_bag = []
        for drv in self.drivers:
            meat = drv().hunt()
            if meat:
                hunting_bag.append(meat)

        content = { "drivers": hunting_bag } 
        f.write(json.dumps(content, indent=4))
        f.close()

    ###########################################################################
    ###########################################################################

    def run(self):
        """Starting point of the platform
        """

        # Check if the hunt mode is enabled
        HUNT = os.getenv('HUNT')
        hunt = os.getenv('hunt')
        self._log.info(f"HUNT={HUNT} & hunt={hunt}")
        if HUNT == "on" or HUNT=="1" or hunt == "on" or hunt=="1":
            self.hunt_mode()

        else:
            # Load a default tree path if not provided
            if not self.tree_filepath:
                # Set the default tree path on linux
                if platform == "linux" or platform == "linux2":
                    self.tree_filepath = f"{self.run_dir}/panduza/tree.json"

            try:
                # Load tree
                self.tree = {}
                with open(self.tree_filepath) as tree_file:
                    self.tree = json.load(tree_file)

                # Parse configs
                self._log.debug(f"load tree:{json.dumps(self.tree, indent=1)}")
                for broker in self.tree["brokers"]:
                    self.__load_tree_broker(self.tree["machine"], broker, self.tree["brokers"][broker])

                # Run all the interfaces on differents threads
                thread_id=0
                for interface in self.interfaces:
                    t = threading.Thread(target=interface["instance"].start, name="T" + str(thread_id))
                    thread_id+=1
                    self.threads.append(t)

                # Start all the threads
                for thread in self.threads:
                    thread.start()

                # Log
                self._log.info("Platform started!")

                # Join them all !
                for thread in self.threads:
                    thread.join()

            except KeyboardInterrupt:
                self._log.warning("ctrl+c => user stop requested")
                self.stop()

            except FileNotFoundError:
                self._log.critical(f"Platform configuration file 'tree.json' has not been found at location '{self.tree_filepath}' !!==>> STOP PLATFORM")

    ###########################################################################
    ###########################################################################

    def stop(self):
        """To stop the entire platform
        """
        # Request a stop for each driver
        for interface in self.interfaces:
            interface["instance"].stop()

        # Join them all !
        for thread in self.threads:
            thread.join()
