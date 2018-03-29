import socket
import hashlib
from enum import Enum
import time


# Available states of client
class States(Enum):
    BUSY_USER, BUILD, WAIT_ANS, FIN_BUILD = range(1, 5)

SYNC_IP = "127.0.0.1"
SYNC_PORT = 1235
MAX_PACKET = 1024
DEFAULT_FILE_PATH = "./collectd.conf"


# Initiate TCP connection with server
sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SYNC_IP, SYNC_PORT))

# Default State
client_state = States.BUSY_USER


################################################
# Helper Methods
################################################
# updates state of client
def update_state(new_state):
    global client_state
    print(client_state, '\t->', new_state)
    client_state = new_state


# returns the checksum of given file
def file_checksum(file_path):
    file = open(file_path, 'rb')
    with file:
        return hashlib.md5(file.read()).hexdigest()

################################################
################################################

# The param should accept file name later
def initiate_build(file_path):
    while client_state != States.FIN_BUILD:
        if client_state == States.BUILD:
            message = file_checksum(file_path)
            sock.sendall(message.encode())
            update_state(States.WAIT_ANS)

        elif client_state == States.WAIT_ANS:
            reply = sock.recv(MAX_PACKET).decode()
            if reply == "DIFF":
                f = open(file_path, 'rb')
                l = f.read(1024)
                while l:
                    print('Sending...')
                    sock.send(l)
                    l = f.read(1024)
                f.close()
            update_state(States.FIN_BUILD)
            time.sleep(5)




# full_path = "./collectd.conf"
# full_path2 = "./collectd2.conf"
#
#
# def file_as_bytes(file):
#     with file:
#         return file.read()
#
# print(hashlib.md5(file_as_bytes(open(full_path, 'rb'))).hexdigest())
# print(hashlib.md5(file_as_bytes(open(full_path2, 'rb'))).hexdigest())


# Assume user runs BUILD
update_state(States.BUILD)

initiate_build(DEFAULT_FILE_PATH)

