from OpenSSL import SSL
import socket
import hmac
from hashlib import sha256

# HMAC Key
PSK_KEY = b"my_shared_key"

# Paths to your certificate and private key
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

# Set up the SSL context
context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_certificate_file(CERT_FILE)
context.use_privatekey_file(KEY_FILE)

# Create a secure socket for the server
def handle_client(ssl_sock):
    try:
        # Step 1: Receive message
        message = ssl_sock.recv(1024)
        
        # Step 2: Receive HMAC
        received_hmac = ssl_sock.recv(64)
        
        # Step 3: Calculate HMAC
        calculated_hmac = hmac.new(PSK_KEY, message, sha256).digest()
        print(f"Received message: {message.decode('utf-8')}")
    
        # Step 4: Validate the HMAC
        if hmac.compare_digest(received_hmac, calculated_hmac):
            print(f"Received valid message: {message.decode('utf-8')}")
            ssl_sock.send(b"Message integrity confirmed.")
        else:
            print("HMAC validation failed.")
            ssl_sock.send(b"HMAC validation failed.")
    finally:
        ssl_sock.shutdown()
        ssl_sock.close()

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 4433))
    sock.listen(5)
    print("Server listening on port 4433...")

    while True:
        client_socket, addr = sock.accept()
        print(f"Connection from {addr}")
        ssl_sock = SSL.Connection(context, client_socket)
        ssl_sock.set_accept_state()
        ssl_sock.do_handshake()  # Perform SSL handshake

        handle_client(ssl_sock)

if __name__ == "__main__":
    start_server()
