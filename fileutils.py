# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   12 April 2018
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.
#
# Description: This file includes utility functions for interacting with the filesystem

import hashlib
import os

slash = "\\" if os.name == "nt" else "/"


def os_path(path):
    return path.replace("/", slash)


def net_path(path):
    return path.replace(slash, "/")


def convert_paths(path_list, fn):
    return [fn(p) for p in path_list]


def get_contents(path, root):
    path = root + slash + path
    with open(os_path(path), "rb") as file:
        return file.read()


def make_directory(path):
    os.makedirs(path, exist_ok=True)


def write_file(file, contents, root):
    file = root + slash + file
    make_directory(os.path.dirname(file))
    with open(os_path(file), "wb") as f:
        f.write(contents)


def delete_file(file, root):
    file = root + slash + file
    os.remove(file)


def file_checksum(path, root):
    return hashlib.md5(get_contents(path, root)).hexdigest()


def list_all_files(root):
    """This function returns all files under the root path, *making sure* not
    to actually include the root part of the path. This is important to enable
    comparing files on two machines where the root parts of the path may differ.

    Ex. Given A/b.txt, A/c.txt, A/D/e.txt, list_all_files(A) returns
    [b.txt, c.txt, D/e.txt].
    """
    local_files = []
    for path, dirs, files in os.walk(os_path(root), followlinks=False):
        if len(files) > 0:
            path_wo_root = path[(len(root) + len(slash)):]  # remove root part
            local_files.extend([os.path.join(path_wo_root, f) for f in files])
    return local_files


def remove_empty_dirs(root):
    for path, _, _ in os.walk(os_path(root), topdown=False):  # bottom up
        if path == root:
            break
        try:
            os.rmdir(path)  # only removes empty directories
        except OSError:
            pass
        else:
            print("Removed dir {}".format(path))


def verify_checksums(files, checksums, root):
    # filters out unchanged files and returns a list of files
    # whose checksums differ from disk
    changed = [f for f, checksum in zip(files, checksums)
               if file_checksum(f, root) != checksum]
    return changed
