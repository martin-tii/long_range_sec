import socket
import struct
import secrets

def create_multicast_announcement():
    multicast_group = 'ff02::1'  # IPv6 multicast address
    multicast_port = 5000

    # Create an IPv6 UDP socket
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    # Set the time-to-live for multicast packets (optional, you can remove this line if not needed)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)

    # Bind the socket to the multicast port (optional, you can remove this line if not needed)
    sock.bind(('::', multicast_port))

    # Generate a 256-bit random ID for the authentication request
    random_id = secrets.token_bytes(32)

    # Combine the ID and message for the authentication request
    message = b'Authentication Request ID: ' + random_id

    # Send the authentication request multicast announcement
    sock.sendto(message, (multicast_group, multicast_port))

    # Set a timeout for waiting for the reply (adjust the value as needed)
    sock.settimeout(5)

    try:
        # Wait for the reply from the authentication server
        data, server_address = sock.recvfrom(1024)
        ip_address = data.decode('utf-8')
        print(f'Received reply from {server_address[0]}: {ip_address}')
    except socket.timeout:
        print('No reply from the authentication server.')

    sock.close()

if __name__ == '__main__':
    create_multicast_announcement()
