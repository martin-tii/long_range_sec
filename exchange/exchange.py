import argparse
import socket
import random

# Define the modulus and base for the Diffie-Hellman key exchange
p = 23
g = 5


def server(port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', port)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            print('connection from', client_address)

            # Send the modulus and base to the client
            connection.sendall(b'%d %d' % (p, g))

            # Receive the client's public key
            client_public_key = int(connection.recv(1024))

            # Calculate Alice's public key and send it to the client
            alice_secret = random.randint(1, p-1)
            alice_public_key = pow(g, alice_secret, p)
            connection.sendall(str(alice_public_key).encode())

            # Calculate the shared secret key
            shared_secret_key = pow(client_public_key, alice_secret, p)
            print('Shared secret key:', shared_secret_key)

            # Receive Bob's public key
            bob_public_key = int(connection.recv(1024))

            # Calculate the shared secret key
            bob_secret = random.randint(1, p-1)
            shared_secret_key = pow(bob_public_key, bob_secret, p)
            print('Shared secret key:', shared_secret_key)

            # Calculate Bob's public key and send it to the client
            bob_public_key = pow(g, bob_secret, p)
            connection.sendall(str(bob_public_key).encode())

        finally:
            # Clean up the connection
            connection.close()


def client(host, port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    server_address = (host, port)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:
        # Receive the modulus and base from the server
        data = sock.recv(1024)
        p, g = [int(x) for x in data.split()]

        # Generate a random secret number for Alice and Bob
        alice_secret = random.randint(1, p-1)

        # Calculate Alice's public key and send it to the server
        alice_public_key = pow(g, alice_secret, p)
        sock.sendall(str(alice_public_key).encode())

        # Receive Bob's public key and calculate the shared secret key
        bob_public_key = int(sock.recv(1024))
        shared_secret_key = pow(bob_public_key, alice_secret, p)
        print('Shared secret key:', shared_secret_key)

        # Calculate Bob's public key and send it to the server
        bob_secret = random.randint(1, p-1)
        bob_public_key = pow(g, bob_secret, p)
        sock.sendall(str(bob_public_key).encode())

    finally:
        # Clean up the socket
        sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Diffie-Hellman key exchange demo')
    parser.add_argument('mode', choices=['server', 'client'], help='run in server or client mode')
