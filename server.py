from OpenSSL import SSL
import hmac
from hashlib import sha256
import socket

PSK_KEY = b"my_shared_key"

# Setting up OpenSSL context
context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_psk_identity_hint(b"iot_device")

def handle_client(client_socket):
    try:
        # Receive message
        message = client_socket.recv(1024)

        # Receive HMAC
        received_hmac = client_socket.recv(64)

        # Calculate HMAC
        calculated_hmac = hmac.new(PSK_KEY, message, sha256).digest()

        # Compare received HMAC with calculated HMAC
        if hmac.compare_digest(received_hmac, calculated_hmac):
            print(f"Received valid message: {message.decode('utf-8')}")
            client_socket.send(b"Message integrity confirmed.")
        else:
            print("HMAC validation failed.")
            client_socket.send(b"HMAC validation failed.")
    finally:
        client_socket.close()

def start_server():
    # Setting up socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('', 4433))
        server_socket.listen(5)
        print("Server listening...")

        while True:
            client_socket, addr = server_socket.accept()
            handle_client(client_socket)

if __name__ == "__main__":
    start_server()
