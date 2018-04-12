# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   <DATE>
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.

import socket
import netutils
import fileutils

TIMEOUT = 60.0
PORT = 0xBDB0  # for buildbox, just for kicks


def run():
    """The entry point for client mode."""

    sock = connect()
    #Assumed protocol:
    #   on connection server does nothing.
    #   on recieving a file list, server returns 2 things in this order
    #       - a list of missing files
    #       - checksums for existing files
    #   on recieving a file, server returns nothing
    #   on building server returns ... ? a single message with relevant data presumably
    inform_filenames(sock)
    missing = netutils.recv_file_list(sock)["files"]
    check = netutils.recv_file_checksums(sock)
    changed = fileutils.verify_checksums(check["files"], check["sums"])
    send_files(sock, missing)
    send_files(sock, changed)
    #no need to send any "done with syncing type thing
    #just send a build command.
    pass


def connect(host):
    # create an INET, STREAMing socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((host, PORT))
    return sock


def inform_filenames(sock):
    filenames = fileutils.list_all_files()
    netutils.send_file_list(sock, filenames)


def send_files(sock, files):
    for f in files:
        netutils.send_file(sock, f)


def sync_file(filename):
    """For now, we will only support file mirroring. This will be
    done for each file as a series of exchanges:
        * Client notifies server of file, with checksum
        * Server tests for file's existence, compares checksum,
          requests file if nonexistent or different, or simply acknowledges
        * Client sends file if requested
    """
    raise NotImplemented

