# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   11 April 2018
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.
#
# Description: This file includes utility functions for communicating
#     across a socket.

import json
import socket


def recvall(sock, n) -> bytes:
    """Helper function to receive exactly n bytes.

    taken from https://docs.python.org/3/howto/sockets.html
    """
    chunks = []
    bytes_recd = 0
    while bytes_recd < n:
        try:
            chunk = sock.recv(min(n - bytes_recd, 2048))
        except socket.timeout:
            chunk = b""
        if chunk == b"":
            raise EOFError()  # reached EOF too early, indicate end-of-stream
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b"".join(chunks)


def send_with_header(sock, header=b"", body=b""):
    """Send two separate pieces of information in one message, recording sizes.

    This function is the sending side of our protocol. It allows us to
    send both raw data and metadata describing the contents of our data.

    The intended usage for this function is to send the header as a JSON
    object, containing a "type" field with the basic type of the message,
    and additional fields as consistent with each "type" value. However,
    this is not enforced here. Limit 2**32 bytes per header, body.
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
    value. However, this is not enforced here.
    """
    sizes = recvall(sock, 8)
    len_header = int.from_bytes(sizes[:4], "big")
    len_data = int.from_bytes(sizes[4:], "big")
    msg = recvall(sock, len_header + len_data)
    header = msg[:len_header]
    body = msg[len_header:]
    return header, body


def send_file(sock, filename, checksum=None):
    """Use send_with_header to send a file's name, checksum, and contents."""
    with open(filename, "rb") as file:  # read binary
        body = file.read()
    metadata = {
        "type": "file",
        "name": filename,
        "checksum": checksum
    }
    header = json.dumps(metadata).encode('utf-8')
    send_with_header(sock, header, body)


def send_file_list(sock, filelist, checksumlist=None):
    """Use send_with_header to send a list of files (and optionally, checksums).
    """
    if checksumlist is not None:
        assert len(filelist) == len(checksumlist)
    metadata = {
        "type": "file_list",
        "files": filelist,
        "checksums": checksumlist
    }
    header = json.dumps(metadata).encode('utf-8')
    send_with_header(sock, header)


def recv_unknown(sock):
    #for use when program can recv one of several things
    header, body = recv_with_header(sock)
    metadata = json.loads(header.decode("utf-8"))
    metadata["body"] = body
    return metadata


def recv_file(sock):
    "Use recv_with_header to receive a file's name, checksum, and contents."
    header, body = recv_with_header(sock)
    metadata = json.loads(header.decode("utf-8"))
    if metadata["type"] != "file":  # type field should be guaranteed
        raise ValueError("Expected file, got {}".format(metadata["type"]))
    # return a dict with "type", "name", "checksum", "body"
    metadata["body"] = body
    return metadata


def recv_file_list(sock):
    """Use recv_with_header to receive a list of files."""
    header, body = recv_with_header(sock)
    metadata = json.loads(header.decode("utf-8"))
    if metadata["type"] != "file_list" or len(body) != 0:
        raise ValueError("Expected file_list, got {}".format(metadata["type"]))
    # return a dict with "type", "files", "checksums" (optionally None)
    return metadata


def recv_file_checksums(sock):
    """Use recv_with_header to receive a list of files and their checksums."""
    metadata = recv_file_list(sock)
    if metadata["checksums"] is None:
        raise ValueError("Expected checksums, got None")
    # return a dict with "type", "files", "checksums"
    return metadata
