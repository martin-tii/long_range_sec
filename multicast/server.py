import socket
import struct

def authentication_server():
    multicast_group = 'ff02::1'  # IPv6 multicast address
    multicast_port = 5000

    # Create an IPv6 UDP socket
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    # Bind the socket to the multicast port
    sock.bind((multicast_group, multicast_port))

    # Join the multicast group on the server side
    group_bin = socket.inet_pton(socket.AF_INET6, multicast_group)
    mreq = group_bin + struct.pack('@I', 0)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    while True:
        try:
            # Receive data from the multicast group
            data, address = sock.recvfrom(1024)

            # Parse the message and extract the ID (assuming the message format is "Authentication Request ID: {32-byte-id}")
            if data.startswith(b'Authentication Request ID:'):
                request_id = data[26:]  # Extract the ID portion of the message

                print(request_id)

                #maybe here will be the auth algorithm

                # Reply with the server's IP address
                server_ip = socket.gethostbyname(socket.gethostname())  # Get the server's IP address
                sock.sendto(server_ip.encode('utf-8'), address)
        except KeyboardInterrupt:
            break

    # Leave the multicast group and close the socket
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_LEAVE_GROUP, mreq)
    sock.close()

if __name__ == '__main__':
    authentication_server()
