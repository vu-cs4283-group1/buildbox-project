import socket
import hashlib
from enum import Enum


# Available states of server
class States(Enum):
    STANDBY, SENT_SAME, SENT_DIFF = range(1, 4)

SYNC_IP = "127.0.0.1"
SYNC_PORT = 1235
MAX_PACKET = 1024
DEFAULT_FILE_PATH = "./collectd2.conf"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SYNC_IP, SYNC_PORT))
sock.listen(1)

# Default State
server_state = States.STANDBY

################################################
# Helper Methods
################################################
# updates state of client
def update_state(new_state):
    global server_state
    print(server_state, '\t->', new_state)
    server_state = new_state


# returns the checksum of given file
def file_checksum(file_path):
    file = open(file_path, 'rb')
    with file:
        return hashlib.md5(file.read()).hexdigest()


def check_file_checksum(file_path, checksum):
    return file_checksum(file_path) == checksum

################################################
################################################

conn, addr = sock.accept()
while True:
    print(" ")
    if server_state == States.STANDBY:
        # Wait for msg from client
        print("Waiting for msg from client")
        checksum = conn.recv(MAX_PACKET).decode()
        message, cur_state = "SAME", States.STANDBY
        if checksum != "" and file_checksum(DEFAULT_FILE_PATH) != checksum:
            message = "DIFF"
            cur_state = States.SENT_DIFF
            print("Files are different")
        conn.sendall(message.encode())
        update_state(cur_state)

    elif server_state == States.SENT_DIFF:
        # receive file from client
        print("Receiving file from client")
        data = conn.recv(MAX_PACKET)
        f = open(DEFAULT_FILE_PATH, 'wb')
        while data:
            f.write(data)
            print("Receiving...")
            data = conn.recv(MAX_PACKET)
        f.close()
        update_state(States.STANDBY)
        print("Finished receiving file")








