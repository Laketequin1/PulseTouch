import socket
import ssl
import ast

# Server settings
HOST = '127.0.0.1'
PORT = 65432

show_warnings = True

def warn(message): # Displays warning/error messages
    if show_warnings == True: # If warning messages active
        print(f"[WARNING] {message}") # Print warning message

def eval_message(message):
    """
    Safely return the eval of a string.
    
    The function attempts to safely return the eval of a string with ast.literal_eval. If the string can not be evaled due to a ValueError then call warn and return None.
    
    This is useful for converting the string with a dictionary inside to just a dictionary, without causing any security risks.

    Parameters
    ----------
    message : string
        A evaluable string.

    Returns
    -------
    any
        The result of the evaled string.
        
    ** ValueError **
    If string cannot be evaled due to ValueError raised:
    
    NoneType
        None.
        
    Examples
    --------
    >>> message = eval_message("{'one':1, 'two':2, 'three':3}")
    >>> print(message)
    {'one':1, 'two':2, 'three':3}

    ** ValueError **
    If string cannot be evaled due to ValueError raised:
    
    >>> message = eval_message("{'one':1, 'two:2, 'three':3}")
    [WARNING] Unable to eval message recieved: "{'one':1, 'two:2, 'three':3}"
    >>> print(message)
    None
    """
    if type(message) == str and message:
        try:
            return ast.literal_eval(message)
        except ValueError:
            warn(f'Unable to eval message recieved: "{message}"')
    elif message:
        warn(f"Message length is 0")
        return ""
    else:
        warn(f"Message type is not str: {type(message)}")
        return None

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
    secure_socket.sendall(b'{"WatchID": 29542649, "WatchActive": True}')

    # Receive data
    raw_data = secure_socket.recv(1024).decode('utf-8')

    data = eval_message(raw_data)

    print(f"Received: {data}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection
    secure_socket.close()
