# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   12 April 2018
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.
#
# Description: This file includes utility functions for interacting with the filesystem

import os
import hashlib


slash = "\\" if os.name == "nt" else "/"


def os_path(path):
    return path.replace("/", slash)


def net_path(path):
    return path.replace(slash, "/")


def get_contents(path, root):
    path = root + slash + path
    with open(os_path(path), "rb") as file:
        return file.read()


def make_directory(path):
    os.makedirs(path, exist_ok=True)


def write_file(path, contents, root):
    path = root + slash + path
    make_directory(os.path.dirname(path))
    with open(os_path(path), "wb") as file:
        file.write(contents)


def file_checksum(path, root):
    return hashlib.md5(get_contents(path, root)).hexdigest()


def list_all_files(root):
    local_files = []
    for path, dirs, files in os.walk(os_path(root), followlinks=False):
        for file in files:
            local_files.append(net_path(path) + slash + file)
    return local_files


def delete_extra_files(files, root):
    local_files = list_all_files(root)
    root_files = [str(root) + "/" + i for i in files]
    extra = set(local_files) - set(root_files)
    for f in extra:
        os.remove(f)
    return extra


def get_missing_files(files, root):
    on_disk = list_all_files(root)
    root_files = [str(root) + "/" + i for i in files]
    missing = list(set(files) - set(on_disk))
    # print(list(set(root_files) - set(on_disk)))
    # print(on_disk)
    return missing


def verify_checksums(files, checksums, root):
    # filters out unchanged files and returns a list of files
    # whose checksums differ from disk
    changed = [f for f, checksum in zip(files, checksums)
               if file_checksum(f, root) != checksum]
    return changed
