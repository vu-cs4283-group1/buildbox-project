# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   <DATE>
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.

import socket
import threading
import netutils
import fileutils

TIMEOUT = 60.0
PORT = 0xBDB0  # for buildbox, just for kicks
LISTENER_COUNT = 5
DEBUG = False

def run():
    """The entry point for server mode."""

    server_socket = setup()
    start(server_socket)


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


def start(server_socket):
    """Continually wait for, accept, and handle connections from clients."""

    try:
        # enter an infinite loop that may be interrupted by pressing ^C
        while True:
            # accept connections from outside
            client_socket, address = server_socket.accept()
            client_socket.settimeout(TIMEOUT)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # let handle_client() handle the request
            ct = threading.Thread(target=handle_client, args=(client_socket, address))
            ct.start()
    except KeyboardInterrupt:
        # safely allow threads to continue their work (this shouldn't take long)
        if threading.activeCount() > 1:
            print("\n*** Stopping server...")
            for t in threading.enumerate():
                if t is not threading.currentThread():
                    t.join(TIMEOUT)
        print("\n*** Server stopped successfully.")
    finally:
        server_socket.close()


def handle_client(sock, address):
    """The function that handles each individual connection.

    Protocol:
    * on connection server does nothing.
    * on receiving a file list, server returns 2 things in this order
        - a list of missing files
        - checksums for existing files
    * on receiving a file, server returns nothing
    * on building server returns a single message with relevant data, presumably
    """

    with sock:
        # do the following for each connection
        print("Handling {}".format(address))
        # use IP address of client as dirname for their code
        root = str(address[0])
        fileutils.make_directory(root)

        files = netutils.recv_file_list(sock)["files"]
        # determine which files the server is missing
        missing = fileutils.get_missing_files(files, root)
        if DEBUG:
            print("Missing: {}".format("\n".join(missing)))
        not_missing = list(set(files) - set(missing))
        if DEBUG:
            print("Have: {}".format("\n".join(missing)))
        # inform the client of missing files and the checksums of existing files
        inform_missing(sock, missing)
        inform_checksums(sock, not_missing, root)

        # receive the list of files the client is about to send
        to_receive = set(netutils.recv_file_list(sock)["files"])
        while len(to_receive) > 0:
            file = netutils.recv_file(sock)
            if file["name"] not in to_receive:
                print("Unexpected file: \"{}\"".format(file["name"]))
            else:
                print("Received file ({} bytes): \"{}\""
                      .format(len(file["body"]), file["name"]))
                fileutils.write_file(file["name"], file["body"], root)
            to_receive.remove(file["name"])

        # send confirmation to the client. TODO run client code
        netutils.send_text(sock, "All files received, done.")
        fileutils.delete_extra_files(files)
        print("All files received, done.")


def inform_missing(sock, files):
    netutils.send_file_list(sock, files)


def inform_checksums(sock, filenames, root):
    checksums = [fileutils.file_checksum(f, root) for f in filenames]
    netutils.send_file_list(sock, filenames, checksums)


def recv_filenames(sock):
    data = netutils.recv_file_list(sock)
    return data["files"]
