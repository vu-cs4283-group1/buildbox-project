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


def run(c_args):
    """The entry point for client mode.

    Protocol:
    * on connection client sends its command line arguments
    * client sends a list of all files in the directory 'root'
    * client receives 2 things in this order
        - a list of missing files
        - checksums for existing files
    * client sends a list of files to send
    * client sends all missing and changed files
    * client receives a single message with relevant data
    """
    host = c_args.host
    root = c_args.root
    sock = connect(host)
    with sock:
        # inform the server of the given command line arguments
        netutils.send_args(sock, c_args)
        # inform the server of local files
        inform_locals(sock, root)
        # determine which files the server is missing
        missing = netutils.recv_file_list(sock)["files"]
        # determine which files are on the server but differ from the client
        check = netutils.recv_file_checksums(sock)
        changed = fileutils.verify_checksums(check["files"], check["checksums"], root)
        # create and send a list of files to be sent
        to_send = missing + changed
        netutils.send_file_list(sock, to_send)
        # send the actual files, order doesn't matter
        for file in to_send:
            if not c_args.quiet:
                print("Sending file:", file)
            netutils.send_file(sock, file)

        # display the final response from the server
        print("remote:", netutils.recv_text(sock))
        if not c_args.no_build and not c_args.dry_run:
            output = netutils.recv_text(sock)
            print(output)


def connect(host):
    # create an INET, STREAMing socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((host, PORT))
    return sock


def inform_locals(sock, root):
    netutils.send_file_list(sock, fileutils.list_all_files(root))
