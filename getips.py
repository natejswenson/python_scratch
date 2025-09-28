import socket
import re

def discover_roku_devices():
    # SSDP Multicast address and port
    MCAST_GRP = '239.255.255.250'
    MCAST_PORT = 1900
    MESSAGE = ('M-SEARCH * HTTP/1.1\r\n' +
               'HOST: 239.255.255.250:1900\r\n' +
               'MAN: "ssdp:discover"\r\n' +
               'MX: 1\r\n' +
               'ST: roku:ecp\r\n\r\n')
    
    # Create the socket for the multicast communication
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(5)
    
    # Allow multiple sockets to use the same PORT number
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Send the message to the multicast group
    sock.sendto(MESSAGE.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
    
    # Listen for responses from Roku devices
    ip_addresses = []
    try:
        while True:
            data, addr = sock.recvfrom(65507)
            response = data.decode('utf-8')
            if 'roku:ecp' in response:
                ip_addresses.append(addr[0])
    except socket.timeout:
        pass
    
    return ip_addresses

# Discover Roku devices on the network
roku_devices = discover_roku_devices()
for i, ip in enumerate(roku_devices, start=1):
    print(f"Roku Device {i}: {ip}")