import subprocess
import time
import psutil

# Define paths to server.py and client.py
server_path = "server.py"
client_path = "client.py"

# Function to check if server.py is already running
def is_server_running():
    for proc in psutil.process_iter():
        try:
            # Check if the process name matches server.py
            if "server.py" in proc.cmdline():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# Launch server.py in a new terminal
if not is_server_running():
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'python3 {server_path}; exec $SHELL'])

    time.sleep(1)

# Launch client.py in a new terminal
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'python3 {client_path}; exec $SHELL'])