# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   <DATE>
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.

import socket
import threading
import os                       # find os type
# from subprocess import call     # run shell commands
import json                     # import json file

import netutils
import fileutils
import commands


TIMEOUT = 60.0
PORT = 0xBDB0  # for buildbox, just for kicks
LISTENER_COUNT = 5


def run(s_args):
    """The entry point for server mode."""
    server_socket = setup()
    start(server_socket, s_args)


def setup():
    """Binds a streaming server socket to the port and starts its listening."""

    server_socket = None
    try:
        # create an INET, STREAMing socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to any address the computer may have
        server_socket.bind(("", PORT))
    except Exception:
        print("*** Failed to start server:")
        if server_socket is not None:
            server_socket.close()
        raise
    # become a server socket
    server_socket.listen(LISTENER_COUNT)
    print("Listening on {}".format(socket.gethostbyname(socket.gethostname())))
    return server_socket


def start(server_socket, s_args):
    """Continually wait for, accept, and handle connections from clients."""

    try:
        # enter an infinite loop that may be interrupted by pressing ^C
        while True:
            # accept connections from outside
            client_socket, address = server_socket.accept()
            client_socket.settimeout(TIMEOUT)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # let handle_client() handle the request
            ct = threading.Thread(target=handle_client, args=(client_socket, address, s_args))
            ct.start()
    except KeyboardInterrupt:
        # safely allow threads to continue their work (this shouldn't take long)
        if threading.activeCount() > 1:
            if not s_args.quiet:
                print("\n*** Stopping server...")
            for t in threading.enumerate():
                if t is not threading.currentThread():
                    t.join(TIMEOUT)
        if not s_args.quiet:
            print("\n*** Server stopped successfully.")
    finally:
        server_socket.close()


def handle_client(sock, address, s_args):
    """The function that handles each individual connection.

    Protocol:
    * on connection server does nothing.
    * on receiving a set of client command line arguments, store them
    * on receiving a file list, server returns 2 things in this order
        - a list of missing files
        - checksums for existing files
    * server receives a set of incoming files
    * on receiving each file, server removes filename from set of incoming files
    * when all files have been received, server starts build
    * on building server returns a single message with relevant data
    """

    with sock:
        # do the following for each connection
        if not s_args.quiet:
            print("-------------------\nHandling {}".format(address))
        # use IP address of client as dirname for their code
        root = str(address[0])

        # get the client's command line arguments, keep c_args, s_args separate
        c_args = netutils.recv_args(sock)
        # get a list of the files in the client's specified directory
        c_files = netutils.recv_file_list(sock)["files"]
        # get a list of the files in the server's root directory
        s_files = fileutils.list_all_files(root)

        # determine which files the server is missing and which should be deleted
        not_missing, missing, extra = categorize_files(c_files, s_files)
        # inform the client of missing files and the checksums of existing files
        netutils.send_file_list(sock, missing)
        # send checksums of existing files
        checksums = [fileutils.file_checksum(f, root) for f in not_missing]
        netutils.send_file_list(sock, not_missing, checksums)

        # receive the actual files from the client
        receive_files(sock, s_args, c_args, root)

        # remove unnecessary files
        remove_extra_files(extra, s_args, c_args, root)

        # send confirmation to the client.
        reply = "All files received.\n"
        if not c_args.no_build:
            reply += "Building.\n"
        if not s_args.quiet:
            print(reply)
        netutils.send_text(sock, reply)

        # run the build
        if not c_args.no_build:
            do_build(sock, s_args, root)
        if not s_args.quiet:
            print("-------------------")


def receive_files(sock, s_args, c_args, root):
    # receive the list of files the client is about to send
    to_receive = set(netutils.recv_file_list(sock)["files"])
    while len(to_receive) > 0:
        file = netutils.recv_file(sock)
        if file["name"] not in to_receive:
            if not s_args.quiet:
                print("Unexpected file: \"{}\"".format(file["name"]))
        else:
            if not s_args.quiet:
                print("Received file ({} bytes): \"{}\""
                      .format(len(file["body"]), file["name"]))
            if not c_args.dry_run:
                fileutils.write_file(file["name"], file["body"], root)
        to_receive.remove(file["name"])


def remove_extra_files(extra, s_args, c_args, root):
    for e in extra:
        if not s_args.quiet:
            print("Deleted file: \"{}\"".format(e))
        if not c_args.dry_run:
            fileutils.delete_file(e, root)


def do_build(sock, s_args, root):
    # build the code and send information to the client
    try:
        return_code, output = commands.run(s_args.file, root)
    except ValueError as v:
        errmsg = v.args[0]
        if not s_args.quiet:
            print(errmsg)
        netutils.send_text(sock, errmsg)
    else:
        if not s_args.quiet:
            print(output.decode("utf-8"))
        # send the build output to the client
        netutils.send_text(sock, output)


def categorize_files(c_files, s_files):
    c_files = set(c_files)
    s_files = set(s_files)
    not_missing = list(c_files & s_files)  # files on both computers
    missing = list(c_files - s_files)  # files on the client but not server
    extra = list(s_files - c_files)  # files on the server but not client
    return not_missing, missing, extra
