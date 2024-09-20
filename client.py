from OpenSSL import SSL
import socket
import hmac
from hashlib import sha256

# HMAC Key
PSK_KEY = b"my_shared_key"

# Path to server certificate
CA_CERT_FILE = 'server.crt'

# Set up the SSL context
context = SSL.Context(SSL.TLSv1_2_METHOD)
context.load_verify_locations(CA_CERT_FILE)

# Create a secure socket for the client
def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = SSL.Connection(context, sock)
    ssl_sock.connect(('127.0.0.1', 4433))
    ssl_sock.set_connect_state()
    ssl_sock.do_handshake()

    # Step 1: Create a message
    message = b"Hello, Server! This is a secure message."
    
    # Step 2: Generate HMAC for the message
    generated_hmac = hmac.new(PSK_KEY, message, sha256).digest()
    
    # Step 3: Send the message and HMAC
    ssl_sock.send(message)
    ssl_sock.send(generated_hmac)
    
    # Step 4: Receive server response
    response = ssl_sock.recv(1024)
    print(f"Sending message: {message}")
    print(f"Server response: {response.decode('utf-8')}")

    ssl_sock.shutdown()
    ssl_sock.close()

if __name__ == "__main__":
    start_client()
