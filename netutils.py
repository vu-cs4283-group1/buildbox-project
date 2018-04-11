# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   <DATE>
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.
#
# Description: This file includes utility functions for communicating
#     across a socket.

import json


def checksum(data):
    # TODO
    raise NotImplemented


def recvall(sock, n):
    """Helper function to receive exactly n bytes.

    taken from https://docs.python.org/3/howto/sockets.html
    """
    chunks = []
    bytes_recd = 0
    while bytes_recd < n:
        chunk = sock.recv(min(n - bytes_recd, 2048))
        if chunk == b'':
            raise EOFError  # reached EOF too early
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks)


def send_with_header(sock, header=b"", body=b""):
    """Send two separate pieces of information in one message, recording sizes.

    This function is the sending side of our protocol. It allows us to
    send both raw data and metadata describing the contents of our data.

    The intended usage for this function is to send the header as a JSON
    object, containing a "type" field with the basic type of the message,
    and additional fields as consistent with each "type" value.
    Limit 2**32 bytes per header, body.
    """
    len_header = len(header)
    len_data = len(body)
    raw_bytes = bytearray(8 + len_header + len_data)  # bytearray is mutable
    raw_bytes[:4] = len_header.to_bytes(4, "big")
    raw_bytes[4:8] = len_data.to_bytes(4, "big")
    raw_bytes[8:8+len_header] = header
    raw_bytes[8+len_header:] = body
    sock.sendall(raw_bytes)


def recv_with_header(sock):
    """Receive two separate pieces of information from one message.

    This function is the receiving side of our protocol. It allows us
    to receive both raw data and metadata describing the contents of
    the data, ensuring that the complete message is received.

    The intended usage for this function is to load the header as a JSON
    object and to use the "type" field to determine the basic type of
    the message, reading additional fields as consistent with the "type"
    value.
    """
    sizes = recvall(sock, 8)
    assert(sizes is not None)
    len_header = int.from_bytes(sizes[:4], "big")
    len_data = int.from_bytes(sizes[4:], "big")
    msg = recvall(sock, len_header + len_data)
    assert(msg is not None)
    header = msg[:len_header]
    body = msg[len_header:]
    return header, body


# uses send_with_header to send a file's name, checksum, and contents
def send_file(sock, filename, send_checksum=False):
    with open(filename, 'rb') as file:  # read binary
        body = file.read()
    metadata = {
        "type": "file",
        "name": filename,
        "checksum": checksum(body) if send_checksum else None
    }

    header = json.dumps(metadata).encode('utf-8')
    send_with_header(sock, header, body)


# uses send_with_header to send a list of files
def send_file_list(sock, filelist):
    metadata = {
        "type": "file_list",
        "files": filelist
    }
    header = json.dumps(metadata).encode('utf-8')
    send_with_header(sock, header)


# uses recv_with_header to receive a file's name, checksum, and contents
def recv_file(sock):
    header, body = recv_with_header(sock)
    metadata = json.loads(header.decode('utf-8'))
    if metadata["type"] != "file":  # type field should be guaranteed
        raise ValueError
    # return a dict with "type", "name", "checksum", "body"
    metadata["body"] = body
    return metadata


# uses recv_with_header to receive a list of files
def recv_file_list(sock):
    header, body = recv_with_header(sock)
    metadata = json.loads(header.decode('utf-8'))
    if metadata["type"] != "file_list" or len(body) != 0:
        raise ValueError
    # return a dict with "type", "files"
    return metadata
