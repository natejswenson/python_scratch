"""Network discovery for Roku devices using SSDP multicast."""
import socket
from typing import List

# SSDP Constants
SSDP_MULTICAST_GROUP = '239.255.255.250'
SSDP_PORT = 1900
SSDP_TIMEOUT = 5
SOCKET_BUFFER_SIZE = 65507

def discover_roku_devices() -> List[str]:
    """
    Discover Roku devices on the local network using SSDP protocol.

    Returns:
        List of IP addresses of discovered Roku devices
    """
    # SSDP discovery message
    message = (
        'M-SEARCH * HTTP/1.1\r\n'
        f'HOST: {SSDP_MULTICAST_GROUP}:{SSDP_PORT}\r\n'
        'MAN: "ssdp:discover"\r\n'
        'MX: 1\r\n'
        'ST: roku:ecp\r\n\r\n'
    )

    # Create the socket for multicast communication
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(SSDP_TIMEOUT)

    # Allow multiple sockets to use the same PORT number
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Send the message to the multicast group
        sock.sendto(message.encode('utf-8'), (SSDP_MULTICAST_GROUP, SSDP_PORT))

        # Listen for responses from Roku devices
        ip_addresses = []
        try:
            while True:
                data, addr = sock.recvfrom(SOCKET_BUFFER_SIZE)
                response = data.decode('utf-8')
                if 'roku:ecp' in response and addr[0] not in ip_addresses:
                    ip_addresses.append(addr[0])
        except socket.timeout:
            pass

        return ip_addresses
    finally:
        sock.close()

def main() -> None:
    """Main function to discover and display Roku devices."""
    roku_devices = discover_roku_devices()

    if roku_devices:
        for i, ip in enumerate(roku_devices, start=1):
            print(f"Roku Device {i}: {ip}")
    else:
        print("No Roku devices found on the network")

if __name__ == "__main__":
    main()