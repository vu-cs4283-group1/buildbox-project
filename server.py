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
    """For now, we will only support file mirroring. This will be
    done for each file as a series of exchanges:
        * Client notifies server of file, with checksum
        * Server tests for file's existence, compares checksum,
          requests file if nonexistent or different, or simply acknowledges
        * Client sends file if requested
    """
    while True:
        #use socket exceptions to break loop or terminate thread once socket is closed?
        data = netutils.recv_unknown(sock)
        if data["type"] == "file":
            fileutils.write_file(data["name"], data["body"])
        elif data["type"] == "file_list":
            files = data["files"]
            fileutils.delete_extra_files(files)
            missing = fileutils.get_missing_files(files)
            not_missing = [f for f in files if f not in missing]
            inform_missing(sock, missing)
            inform_checksums(sock, not_missing)
        else:
            raise NotImplemented #or a different error


def inform_missing(sock, files):
    netutils.send_file_list(sock, files)


def inform_checksums(sock, filenames):
    checksums = [fileutils.file_checksum(f) for f in filenames]
    netutils.send_file_checksums(sock, filenames, checksums)


def recv_filenames(sock):
    data = netutils.recv_file_list(sock)
    return data["files"]


# Shut down and close the given socket.
def cleanup(sock):
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()