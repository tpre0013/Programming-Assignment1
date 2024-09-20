from mbedtls import tls, PSK
from mbedtls.tls import ServerContext, TLSConfiguration

# Define a pre-shared key and identity for the devices
PSK_IDENTITY = b"iot_device"
PSK_KEY = b"my_shared_key"

# Create server configuration
config = TLSConfiguration(pre_shared_key=(PSK_IDENTITY, PSK_KEY))

# Set up the server context
server_context = ServerContext(config)

def start_server():
    with server_context.wrap_socket(('', 4433), server_side=True) as sock:
        print("Server listening...")
        while True:
            client, addr = sock.accept()
            print(f"Connection established with {addr}")
            message = client.recv(1024)
            print(f"Received: {message}")
            client.send(b"Secure communication established!")
            client.close()

if __name__ == "__main__":
    start_server()
