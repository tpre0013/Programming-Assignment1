from OpenSSL import SSL
import hmac
from hashlib import sha256
import socket

PSK_KEY = b"my_shared_key"

def start_client():
    # Setting up socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 4433))

        # Create the message
        message = b"Hello, Server! This is a secure message."

        # Generate the HMAC for the message
        generated_hmac = hmac.new(PSK_KEY, message, sha256).digest()

        # Send the message and its HMAC
        client_socket.send(message)
        client_socket.send(generated_hmac)

        # Receive server response
        response = client_socket.recv(1024)
        print(f"Server response: {response.decode('utf-8')}")

if __name__ == "__main__":
    start_client()
