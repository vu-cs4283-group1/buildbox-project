# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   <DATE>
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.

import socket
import threading

TIMEOUT = 60.0


# Binds a streaming server socket to the port and starts its listening.
def setup_server(port, listener_count):
    server_socket = None
    try:
        # create an INET, STREAMing socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to any address the computer may have
        server_socket.bind(("", port))
    except Exception as e:
        print("*** Failed to start server:")
        if server_socket is not None:
            server_socket.close()
        raise e
    # become a server socket
    server_socket.listen(listener_count)
    return server_socket


def start_server(server_socket):
    try:
        # enter an infinite loop that may be interrupted by pressing ^C
        while True:
            # accept connections from outside
            (client_socket, address) = server_socket.accept()
            client_socket.settimeout(TIMEOUT)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # let handle_client() handle the request
            ct = threading.Thread(target=handle_client, args=(client_socket, address))
            ct.run()
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


def handle_client(client_socket, address):
    # TODO
    pass


# Shut down and close the given socket.
def cleanup(sock):
    assert isinstance(sock, socket.socket)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()