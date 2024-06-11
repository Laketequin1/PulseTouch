import socket
import ssl
import ast
import sqlite3
from datetime import datetime, timedelta

# Server settings
HOST = '127.0.0.1'
PORT = 65432

show_warnings = True

conn = sqlite3.connect('PulseTouch.db')

cur = conn.cursor()

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
    elif type(message) != str:
        warn(f"Message type is not str: {type(message)}")
        return ""
    else:
        warn(f"Message length is 0")
        return None

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Secure the socket with SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='server_cert.pem', keyfile='server_key.pem')

# Bind and listen
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

try:
    # Create table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS WatchStatus (
        EventID INTEGER PRIMARY KEY AUTOINCREMENT,
        GroupID INTEGER NOT NULL,
        WatchID INTEGER NOT NULL,
        ActivationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        ActivationEvent BOOLEAN NOT NULL
    );
    ''')

    conn.commit()
except Exception as e:
    conn.rollback()
    print(f"Transaction failed: {e}")

while True:
    # Accept a connection
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Wrap the socket with SSL
    secure_socket = context.wrap_socket(client_socket, server_side=True)

    connected = True

    try:
        while connected:
            # Receive data
            raw_data = secure_socket.recv(1024).decode('utf-8')

            data = eval_message(raw_data)

            print(f"Received: {data}")

            try:
                cur.execute('''
                INSERT INTO WatchStatus (GroupID, WatchID, ActivationEvent) VALUES (?, ?, ?)
                ''', (data["GroupID"], data["WatchID"], data["ActivationEvent"]))

                conn.commit()

                # Query the database
                cur.execute('''
                            SELECT * 
                            FROM WatchStatus 
                            WHERE GroupID = ? 
                            AND NOT WatchID = ? 
                            AND ActivationTime >= datetime('now', '-2 minutes') 
                            ORDER BY ActivationTime DESC 
                            LIMIT 10
                            ''', (data["GroupID"], data["WatchID"]))
                rows = cur.fetchall()

                for row in rows:
                    print(row)
            except Exception as e:
                conn.rollback()
                print(f"Transaction failed: {e}")

            # Send data
            secure_socket.sendall(b'{"ActivationEvent": True}')

    except Exception as e:
        print(f"Error: {e}")
        connected = False

    finally:
        # Close the connection
        secure_socket.close()