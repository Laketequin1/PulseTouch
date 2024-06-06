import socket
import ssl

# Server settings
HOST = '127.0.0.1'
PORT = 65432

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Secure the socket with SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='server_cert.pem', keyfile='server_key.pem')

# Bind and listen
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

while True:
    # Accept a connection
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Wrap the socket with SSL
    secure_socket = context.wrap_socket(client_socket, server_side=True)

    try:
        # Receive data
        data = secure_socket.recv(1024).decode('utf-8')
        print(f"Received: {data}")

        # Send data
        secure_socket.sendall(b'Hello, client')

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        secure_socket.close()
