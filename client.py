import socket
import ssl

# Server settings
HOST = '127.0.0.1'
PORT = 65432

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Secure the socket with SSL
context = ssl.create_default_context()
context.load_verify_locations('server_cert.pem')

# Connect to the server
secure_socket = context.wrap_socket(client_socket, server_hostname=HOST)
secure_socket.connect((HOST, PORT))

try:
    # Send data
    secure_socket.sendall(b'Hello, server')

    # Receive data
    data = secure_socket.recv(1024).decode('utf-8')
    print(f"Received: {data}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection
    secure_socket.close()
