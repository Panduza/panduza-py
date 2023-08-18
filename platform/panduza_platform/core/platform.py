import os
import sys
import time
import json
import pkgutil
import argparse
import traceback
import threading
import importlib

from sys import platform

from .conf import PLATFORM_VERSION
from log.platform import platform_logger

from .platform_thread import PlatformThread
from .platform_client import PlatformClient
from .platform_errors import InitializationError

from .platform_driver_factory import PlatformDriverFactory
from .platform_device_factory import PlatformDeviceFactory

class Platform:
    """ Main class to manage the platform
    """

    # ---

    def __init__(self, run_dir="/etc"):
        """ Constructor
        """
        # Init the platform logger
        self.log = platform_logger()
        self.run_dir = run_dir

        # Debug logs to structure log file
        self.log.info("==========================================")
        self.log.info(f"= PANDUZA PYTHON PLATFORM          {PLATFORM_VERSION} =")
        self.log.info("==========================================")

        # Create Factories
        self.driver_factory = PlatformDriverFactory(self)
        self.device_factory = PlatformDeviceFactory(self)

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

    # ###########################################################################
    # ###########################################################################

    def load_tree_overide(self, tree_filepath):
        """platform will use the given tree filepath
        """
        self.tree_filepath = tree_filepath
        self.log.debug(f"force tree:{self.tree_filepath}")

    # ###########################################################################
    # ###########################################################################

    # def parse_args(self):
    #     """
    #     """
    #     # Manage arguments
    #     parser = argparse.ArgumentParser(description='Manage Panduza Platform')
    #     parser.add_argument('-t', '--tree', help='path to the panduza tree (*.json)', metavar="FILE")
    #     parser.add_argument('-l', '--log', dest='enable_logs', action='store_true', help='start the logs')
    #     args = parser.parse_args()

    #     # Check if logs are enabled
    #     if not args.enable_logs and self.force_log != True:
    #         self.log.remove()

    #     # Check tree filepath value
    #     self.tree_filepath = args.tree

    # ###########################################################################
    # ###########################################################################

    # def __load_tree_broker(self, machine, broker_name, broker_tree):
    #     """ Load interfaces declared in the tree for the given broker
    #     """
    #     # Debug log
    #     self.log.info(f" + {broker_name} ({broker_tree['addr']}:{broker_tree['port']})")

    #     # Create broker object
    #     broker = Broker(broker_tree["addr"], broker_tree["port"])

    #     # For each interface create it
    #     for interface in broker_tree["interfaces"]:
    #         self.__interpret_interface_declaration(machine, broker, interface)

    #     # Append the platform interface on each managed broker
    #     self.__interpret_interface_declaration(machine, broker, {
    #         "name": "py",
    #         "group": "platform",
    #         "driver": "py.platform"
    #     })

    # ###########################################################################
    # ###########################################################################

    # def __replace_r_with_param(self, element, param):
    #     """
    #     """
    #     # If the element is a dict, replace on each value (not in the keys)
    #     if isinstance(element, dict):
    #         new_dict = {}
    #         for key in element:
    #             new_dict[key] = self.__replace_r_with_param(element[key], param)
    #         return new_dict

    #     # If the element is a string, replace %r with param
    #     elif isinstance(element, str):
    #         return element.replace("%r", str(param))


    #     # TODO
    #     # if element is arry

    # ###########################################################################
    # ###########################################################################

    # def __interpret_interface_declaration(self, machine, broker, interface_declaration):
    #     """ Interpret option in the interface declaration

    #     Options are
    #     - disabled: to prevent this interface from beeing loaded
    #     - repeated: to execute the interface loading multiple times
    #     """
    #     # Check if the interface is disabled by the user
    #     if "disabled" in interface_declaration and interface_declaration["disabled"] == True:
    #         name = "?"
    #         if "name" in interface_declaration:
    #             name = interface_declaration["name"]
    #         driver_name = "?"
    #         if "driver" in interface_declaration:
    #             driver_name = interface_declaration["driver"]
    #         self.log.warning(f"> {name} [{driver_name}] interface disabled")
    #         return

    #     # Multiple interfaces, need to create one interface for each
    #     if "repeated" in interface_declaration:
    #         for param in interface_declaration["repeated"]:
    #             formated_interface_info = self.__replace_r_with_param(interface_declaration, param)
    #             self.__load_interface(machine, broker, formated_interface_info)

    #     # Only one interface to start
    #     else:
    #         self.__load_interface(machine, broker, interface_declaration)


    # ###########################################################################
    # ###########################################################################

    # def register_driver_plugin_discovery(self):
    #     """Function to discover python plugins related to panduza python platform
    #     """
    #     #
    #     # self.log.debug(f"PYPATH: {sys.path}")
    #     # help('modules')

    #     # Discovering process
    #     self.log.debug("Start plugin discovery")
    #     discovered_plugins = {
    #         name: importlib.import_module(name)
    #         for finder, name, ispkg
    #         in pkgutil.iter_modules()
    #         if name.startswith("panduza_class")
    #     }
    #     self.log.debug(f"Discovered plugins: {str(discovered_plugins)}")

    #     # Import plugin inside the platform manager
    #     # Each class plugins export a PZA_DRIVERS_LIST with the list of all the managed drivers
    #     for plugin_name in discovered_plugins :
    #         self.log.info(f"Load plugin: '{plugin_name}'")
    #         plugin_package = __import__(plugin_name)
    #         for drv in plugin_package.PZA_DRIVERS_LIST:
    #             self.register_driver(drv)

    #     # Register drivers already packaged with the platform
    #     for drv in STD_DRIVERS:
    #         self.register_driver(drv)
    #     for drv in FAKE_DRIVERS:
    #         self.register_driver(drv)
    #     for drv in INBUILT_DRIVERS:
    #         self.register_driver(drv)
    #     for drv in FTDI_DRIVERS:
    #         self.register_driver(drv)
    #     for drv in AARDVARK_DRIVERS:
    #         self.register_driver(drv)





    def panic(self):
        """
        """
        self.__alive = False


    ###########################################################################
    ###########################################################################
    ### PUBLIC
    ###########################################################################
    ###########################################################################

    # --

    def run(self):
        """Starting point of the platform
        """
        try:
            # First go into factories initialization
            self.driver_factory.discover()
            self.device_factory.discover()

        except InitializationError as e:
            self.log.critical(f"Error during platform initialization: {e}")
            sys.exit(-1)

        # Check if the hunt mode is enabled
        start_time = time.time()
        if self.__hunt_mode_requested():
            self.__hunt_mode()
        else:
            self.__oper_mode()

        alive_time = round(time.time()-start_time, 2)
        self.log.info(f"Platform alive time {alive_time}s")

    # --

    def load_interface(self, bench_name, device_name, interface_config):
        """Load a new interface
        """
        instance = self.driver_factory.produce_interface(bench_name, device_name, interface_config)
        self.interfaces.append(instance)

    # --

    def get_interface_number(self):
        """
        """
        return len(self.interfaces)

    # --

    def get_interface_instance(self, bench, device, name):
        """Find the interface corresponding the given parameters

        Return the found interface obj, None if not found
        """
        # Go through all interfaces and search for a match
        for itf in self.interfaces:
            same_bench = (itf.bench_name == bench)
            same_device = (itf.device_name == device)
            same_name = (itf.name == name)
            if same_bench and same_device and same_name:
                return itf
        return None

    ###########################################################################
    ###########################################################################
    ### PRIVATES
    ###########################################################################
    ###########################################################################

    # --

    def __hunt_mode_requested(self):
        """Return true if the hunt mode has been requested
        """
        HUNT = os.getenv('HUNT')
        hunt = os.getenv('hunt')
        self.log.info(f"Hunt Flags : HUNT={HUNT} & hunt={hunt}")
        if HUNT == "on" or HUNT == "1" or hunt == "on" or hunt == "1":
            return True
        return False

    # --

    def __oper_mode(self):
        """Run the operational mode

        First all the static aspects are resolved.
        The number of instances, clients and thread are fixed for the rest of the execution.

        Then the dynamic aspect starts
        Threads are started and worker are bring to life
        """
        try:
            self.__load_tree()
            
            
            self.__load_devices()
            
            
            self.load_interface("server", "platforms", {
                    "name": "py",
                    "driver": "py.platform"
                })


            # modify interfaces with tree bench configs

            # create clients

            client = PlatformClient("localhost", 1883)

            # attach interface to client

            # attach clients   to thread


            for interface in self.interfaces:
                interface.attach_pclient(client)

            # Prepare interface internal data
            for interface in self.interfaces:
                interface.initialize()

            # Create and start thread pool
            t = PlatformThread(self)
            self.threads.append(t)

            # attach clients to thread
            self.threads[0].attach_worker(client)

            # attach interfaces to thread
            for interface in self.interfaces:
                self.threads[0].attach_worker(interface)

            # 
            for thr in self.threads:
                thr.start()

            self.__alive = True
            while self.__alive:
                time.sleep(0.1)

            self.__stop()

    #             # Run all the interfaces on differents threads
    #             thread_id=0
    #             for interface in self.interfaces:
    #                 t = threading.Thread(target=interface["instance"].start, name="T" + str(thread_id))
    #                 thread_id+=1
    #                 self.threads.append(t)

    #             # Start all the threads
    #             for thread in self.threads:
    #                 thread.start()

    #             # Log
    #             self.log.info("Platform started!")

    #             # Join them all !
    #             for thread in self.threads:
    #                 thread.join()

        except InitializationError as e:
            self.log.critical(f"Error during platform initialization: {e}")
        except KeyboardInterrupt:
            self.log.warning("ctrl+c => user stop requested")
            self.__stop()
        except FileNotFoundError:
            self.log.critical(f"Platform configuration file 'tree.json' has not been found at location '{self.tree_filepath}' !!==>> STOP PLATFORM")

    # --

    def __stop(self):
        """To stop the entire platform
        """
        self.__alive = False

        # 
        self.log.warning("Platform stopping...")
        for thr in self.threads:
            thr.stop()

        # 
        for thr in self.threads:
            thr.join()

        # Generate status reports
        self.generate_status_reports()


    # --

    def generate_status_reports(self):
        """Generate a json report status and log it to the console
        """

        # Gather the status of each thread
        thread_status = []
        for thr in self.threads:
            thread_status.append(thr.get_status())

        # Write the status file
        with open("/etc/panduza/log/status.json", "w") as json_file:
            json.dump(thread_status, json_file)

        # Print into the console
        report  = "\n"
        for thr in thread_status:
            report += "=================================\n"
            report +=f"== {thr['name']} \n"
            report += "=================================\n"

            for w in thr['workers']:
                report += "\n"
                report += str(w.get("name", "")) + "\n"
                report += str(w.get("final_state", "")) + "\n"
                report += str(w.get("error_string", "")) + "\n"
        self.log.info(report)

    # --

    def __hunt_mode(self):
        """Fonction to perform the interface auto-detection on the system
        """
        self.log.info("*********************************")
        self.log.info("*** !!! HUNT MODE ENABLED !!! ***")
        self.log.info("*********************************")

    #     os.makedirs(f"{self.run_dir}/panduza/platform", exist_ok=True)
    #     filepath_drivers = f"{self.run_dir}/panduza/platform/py_drivers.json"
    #     filepath_instances = f"{self.run_dir}/panduza/platform/py_instances.json"

    #     # Hunt data for each driver
    #     hunting_bag_driver = []
    #     hunting_bag_instances = []
    #     for drv in self.drivers:
    #         self.log.info(f"Hunt with: {drv()._PZA_DRV_config()['name']}")
    #         driver, instances = drv().hunt()
    #         if driver:
    #             hunting_bag_driver.append(driver)
    #         if instances:
    #             hunting_bag_instances.extend(instances)

    #     # Write data into files
    #     with open(filepath_drivers, "w") as f:
    #         f.write(json.dumps(hunting_bag_driver, indent=4))
    #     with open(filepath_instances, "w") as f:
    #         f.write(json.dumps(hunting_bag_instances, indent=4))


    # --

    def __load_tree(self):
        """Load the configuration tree into python object
        """
        # Load a default tree path if not provided
        if not self.tree_filepath:
            # Set the default tree path on linux
            if platform == "linux" or platform == "linux2":
                self.tree_filepath = f"{self.run_dir}/panduza/tree.json"

        # Load tree
        self.tree = {}
        with open(self.tree_filepath) as tree_file:
            self.tree = json.load(tree_file)

        # Parse configs
        self.log.debug(f"load tree:{json.dumps(self.tree, indent=1)}")

    # --

    def __load_devices(self):
        """Load interfaces from device configurations
        """
        # Example
        # device_cfg =
        # {
        #    "model": "Panduza.FakePsu"
        # }
        for device_cfg in self.tree["devices"]:

            # device == class type for device
            device = self.device_factory.produce_device(device_cfg)

            device_name = device_cfg["model"].replace(".", "_")

            interfaces = device._PZA_DEV_interfaces()
            self.log.info(f"{device_name} => {interfaces}")
            for interface_config in interfaces:
                self.load_interface("default", device_name, interface_config)


