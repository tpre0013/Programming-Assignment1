import hmac
from hashlib import sha256
from mbedtls import tls, PSK
from mbedtls.tls import ServerContext, TLSConfiguration

PSK_IDENTITY = b"iot_device"
PSK_KEY = b"my_shared_key"

# Create server configuration
config = TLSConfiguration(pre_shared_key=(PSK_IDENTITY, PSK_KEY))
server_context = ServerContext(config)

def handle_client(client_socket):
    try:
        # Step 1: Receive message
        message = client_socket.recv(1024)
        
        # Step 2: Receive HMAC (Assuming it's sent as a separate message)
        received_hmac = client_socket.recv(64)  # 64 bytes HMAC (SHA-256 output size)

        # Step 3: Calculate HMAC on the server side
        calculated_hmac = hmac.new(PSK_KEY, message, sha256).digest()

        # Step 4: Compare received HMAC with calculated HMAC
        if hmac.compare_digest(received_hmac, calculated_hmac):
            print(f"Received valid message: {message.decode('utf-8')}")
            client_socket.send(b"Message integrity confirmed.")
        else:
            print("HMAC validation failed.")
            client_socket.send(b"HMAC validation failed.")
    finally:
        client_socket.close()

def start_server():
    with server_context.wrap_socket(('', 4433), server_side=True) as sock:
        print("Server listening...")
        while True:
            client, addr = sock.accept()
            handle_client(client)

if __name__ == "__main__":
    start_server()

