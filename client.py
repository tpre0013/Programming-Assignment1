import hmac
from hashlib import sha256
from mbedtls import tls, PSK
from mbedtls.tls import ClientContext, TLSConfiguration

PSK_IDENTITY = b"iot_device"
PSK_KEY = b"my_shared_key"

# Create client configuration
config = TLSConfiguration(pre_shared_key=(PSK_IDENTITY, PSK_KEY))
client_context = ClientContext(config)

def start_client():
    with client_context.wrap_socket(('127.0.0.1', 4433)) as sock:
        # Step 1: Create the message
        message = b"Hello, Server! This is a secure message."
        
        # Step 2: Generate the HMAC for the message
        generated_hmac = hmac.new(PSK_KEY, message, sha256).digest()

        # Step 3: Send the message and its HMAC
        sock.send(message)
        sock.send(generated_hmac)
        
        # Step 4: Receive the server's response
        response = sock.recv(1024)
        print(f"Server response: {response.decode('utf-8')}")

if __name__ == "__main__":
    start_client()
