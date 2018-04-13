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


def run(host):
    """The entry point for client mode.

    Protocol:
    * on connection client sends a file list
    * client receives 2 things in this order
        - a list of missing files
        - checksums for existing files
    * client sends all missing and changed files
    * client receives a single message with relevant data, presumably
    """

    sock = connect(host)
    with sock:
        inform_filenames(sock)
        missing = netutils.recv_file_list(sock)["files"]
        check = netutils.recv_file_checksums(sock)
        changed = fileutils.verify_checksums(check["files"], check["checksums"])
        send_files(sock, missing)
        send_files(sock, changed)
        # TODO no need to send any "done syncing" message, just a build command.


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
