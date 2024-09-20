from mbedtls import tls, PSK
from mbedtls.tls import ClientContext, TLSConfiguration

# Define the same PSK and identity for the client
PSK_IDENTITY = b"iot_device"
PSK_KEY = b"my_shared_key"

# Create client configuration
config = TLSConfiguration(pre_shared_key=(PSK_IDENTITY, PSK_KEY))

# Set up the client context
client_context = ClientContext(config)

def start_client():
    with client_context.wrap_socket(('127.0.0.1', 4433)) as sock:
        sock.send(b"Hello, Server!")
        response = sock.recv(1024)
        print(f"Server response: {response}")

if __name__ == "__main__":
    start_client()
