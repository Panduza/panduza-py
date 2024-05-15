import re
import socket, json, time
import logging


import panduza.core.log

# ┌────────────────────────────────────────┐
# │ Local broker discovery                 │
# └────────────────────────────────────────┘

class Panduza_local_broker_discovery:

    # Should be with other consts 
    PORT_LOCAL_DISCOVERY = 53035
        

    def panduza_local_broker_discovery():
        """ Return the addresses of brokers discover on the local network 

            Raises:
                Exception: raise if connection alias not loaded

            Returns:
                List[str, int]: url, port
        """

        broker_addrs = []

        # Get every network interfaces
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        ips = [ip[-1][0] for ip in interfaces]

        request_payload = json.dumps({"search": True})
        request_payload_utf8 = request_payload.encode(
            encoding="utf-8"
        )

        for ip in ips:
            try: 
                # Send broadcast local discovery request on the local networks
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  
                sock.setblocking(False)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.bind((ip, 0))
                sock.sendto(request_payload_utf8, ("255.255.255.255", Panduza_local_broker_discovery.PORT_LOCAL_DISCOVERY))
                time.sleep(1)
        
                answer_payload, broker_addr = sock.recvfrom(1000)

                # Get the name in the payload 
                json_answer = answer_payload.decode(
                    encoding="utf-8"
                )
                
                # add the platform addr, port and name to the list of broker detected
                broker_addrs.append((broker_addr, json.loads(json_answer)['name']))
            except Exception as e:
                pass
            
            sock.close()
        
        return broker_addrs

    def get_broker_info_with_name(platform_name):
        """ Get the broker info of the first platform found on the 
        local network with the given name

        Arg:
            - platform_name (str, required): name of the platform.
        """

        # Find the platform with the platform name asked 
        url = None
        port = None
        list_info_brokers = Panduza_local_broker_discovery.panduza_local_broker_discovery()
        for info_broker in list_info_brokers:
            platform_name_detected = info_broker[1]
            if (platform_name_detected == platform_name):
                url = info_broker[0][0]
                port = 1883
                # self.port = info_broker[0][1]

        # If any platform find with the given platform_name raise a error 
        if (url == None or port == None):
            raise NameError("Any platform find on the local platform with the name: " + platform_name)
        
        return url, port

    def get_first_broker_info():
        """ Get the broker info of the first platform found on the 
        local network with the given name
        """

        list_info_brokers = Panduza_local_broker_discovery.panduza_local_broker_discovery()
        if (len(list_info_brokers) == 0):
            # Maybe create a exception class for not findind local platform
            raise Exception("Any platform find on the local platform with the name")
        else:
            # If at least one platform find use the first 
            # broker addr and port of the first platform discover
            addr_port = list_info_brokers[0][0]
            url = addr_port[0]

            # Need to change the local discovery of the platform to get port 
            # of broker and not the platform, for the moment use port 1883 

            # self.port = addr_port[1]
            port = 1883

        return url, port


# Create the logger for core events
CoreLog = logging.getLogger(f"pza.core")

# ┌────────────────────────────────────────┐
# │ AliasError                             │
# └────────────────────────────────────────┘

class AliasError(Exception):
    """Error that is raised when a error occurs on the alias management
    """
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)








# ┌────────────────────────────────────────┐
# │ Core                                   │
# └────────────────────────────────────────┘

class Core:
    """Core object to share configuration data
    """

    # Store aliases
    Aliases = {}

    # Store connections data
    Connections = {}

    ###########################################################################
    ###########################################################################

    def LoadAliases(connections=None, json_filepath=None):
        """Load aliases from connections OR json file with connections

        Args:
            connections (dict, optional): Connections as declared as dict
                {
                    "connection_1": {
                        "url": "localhost",
                        "port": 1883,
                        "interfaces": {
                            "foo1": "/topic/to/foo1",
                            "foo2": "/topic/to/foo2",
                        }
                    },
                    "connection_2": {
                        "url": "broker.online",
                        "port": 1883,
                        "interfaces": {
                            "foo3": "/topic/to/foo3",
                            "foo4": "/topic/to/foo4",
                        }
                    }
                }
                Defaults to Null.
            
            json_filepath (string, optional): File containing json connections declaration. Defaults to Null.
        """
        if connections:
            if type(connections) == str:
                connections = json.loads(connections)
            Core.__LoadAliasesFromDict(connections)
        elif json_filepath:
            Core.__LoadAliasesFromFile(json_filepath)

    ###########################################################################
    ###########################################################################

    def __LoadAliasesFromFile(json_filepath):
        """Load aliases from a json file
        """
        try:
            CoreLog.info(f"Load aliases from file : {json_filepath}")
            with open(json_filepath) as f:
                data = json.load(f)
                Core.__LoadAliasesFromDict(data)
        except json.decoder.JSONDecodeError as e:
            raise AliasError("File content is not json well formated")

    ###########################################################################
    ###########################################################################

    def __LoadAliasesFromDict(connections):
        """Load aliases from a connections dict
        """
        # Go through connections and sort them into internal attributes
        CoreLog.info(f"Load aliases from dict : {connections}")
        for co_name, co_data in connections.items():

            # Load connection
            CoreLog.info(f"   Load connection : {co_name} & {co_data}")
            
            # if url and port precise inside alias config use it 
            if ("url" in co_data.keys()) and ("port" in co_data.keys()):
                Core.Connections[co_name] = {
                    "url": co_data["url"],
                    "port": co_data["port"]
                }
            # Use the local discovery to find the broker link to the platform 
            # with the given name
            elif ("platform_name" in co_data.keys()):
                url, port = Panduza_local_broker_discovery.get_broker_info_with_name(co_data["platform_name"])
                Core.Connections[co_name] = {
                    "url": url,
                    "port": port
                }
            # Use the local discovery to find the first platform discovered
            else:
                url, port = Panduza_local_broker_discovery.get_first_broker_info()
                Core.Connections[co_name] = {
                    "url": url,
                    "port": port
                }

            # create automaticaly url,

            # Load aliases
            for it in co_data["interfaces"]:
                CoreLog.info(f"      Load interface : {it}")
                Core.Aliases[it] = {
                    "co": co_name,
                    "base_topic": co_data["interfaces"][it]
                }

    ###########################################################################
    ###########################################################################

    def BrokerInfoFromBrokerAlias(alias):
        """Return the broker data from alias

        Args:
            alias (str): Broker alias

        Raises:
            Exception: raise if connection alias not loaded

        Returns:
            str, int: url, port
        """
        # Get data from the connection
        if alias not in Core.Connections.keys():
            raise Exception("Connection [" + alias + "] not defined")

        # Get the client
        return Core.Connections[alias]["url"], Core.Connections[alias]["port"]

    ###########################################################################
    ###########################################################################

    def BrokerInfoFromInterfaceAlias(alias):
        """Return the broker information to reach the interface from its alias
        """
        # Get alias
        if alias not in Core.Aliases.keys():
            raise Exception("Alias [" + alias + "] not defined")
        co = Core.Aliases[alias]["co"]

        # Get data from the connection
        if co not in Core.Connections.keys():
            raise Exception("Connection [" + co + "] not defined")

        # Get the client
        return Core.Connections[co]["url"], Core.Connections[co]["port"]

    ###########################################################################
    ###########################################################################

    def BaseTopicFromAlias(alias):
        """Return the base topic of the interface from its alias
        """
        # Get alias
        if alias not in Core.Aliases.keys():
            raise Exception("Alias [" + alias + "] not defined")

        return Core.Aliases[alias]["base_topic"]

    ###########################################################################
    ###########################################################################

    def EnableLogging(level=logging.DEBUG):
        panduza.core.log.PZA_LOG_LEVEL = level
        logging.getLogger().setLevel(panduza.core.log.PZA_LOG_LEVEL)


