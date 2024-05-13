import socket, json, time

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
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  
            sock.setblocking(False)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind((ip, 0))
            sock.sendto(request_payload_utf8, ("255.255.255.255", PORT_LOCAL_DISCOVERY))
            time.sleep(1)
       
            answer_payload, broker_addr = sock.recvfrom(1000)
            # add the platform addr and port to the list of broker detected
            broker_addrs.append((broker_addr))
        except Exception as e:
            pass
        
        sock.close()
    
    return broker_addrs