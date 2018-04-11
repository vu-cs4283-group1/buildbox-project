# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   <DATE>
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.

import socket

TIMEOUT = 60.0
PORT = 0xBDB0  # for buildbox, just for kicks


def run():
    """The entry point for client mode."""

    sock = connect()
    pass


def connect(host):
    # create an INET, STREAMing socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((host, PORT))
    return sock


def sync_file(filename):
    """For now, we will only support file mirroring. This will be
    done for each file as a series of exchanges:
        * Client notifies server of file, with checksum
        * Server tests for file's existence, compares checksum,
          requests file if nonexistent or different, or simply acknowledges
        * Client sends file if requested
    """
    raise NotImplemented

