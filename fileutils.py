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
import subprocess

slash = "\\" if os.name == "nt" else "/"
cur_path = os.path.dirname(os.path.realpath(__file__)) + slash


def get_contents(path):
    with open(path, "rb") as file:
        return file.read()


def write_file(path, contents):
    with open(path, "wb") as file:
        file.write(contents)


def file_checksum(path):
    return hashlib.md5(get_contents(path)).hexdigest()


def list_all_files(path):
    all = []
    my_path = cur_path + path

    for path, dirs, files in os.walk(my_path):
        for file in files:
            if file[0] != ".":
                formatted_path = path[len(my_path):] + slash if len(my_path) != len(path) else ""
                all.append(formatted_path + file)
    return all


def delete_extra_files(path, files):
    my_files = list_all_files(path)
    diff_files = list(set(my_files) - set(files))
    for inv_file in diff_files:
        formatted_path = path + slash if path != "" else ""
        os.remove(formatted_path + inv_file)


def get_missing_files(files):
    raise NotImplemented


def verify_checksums(files, checksums):
    # filters out unchanged files and returns a list of files
    # whose checksums differ from disk
    changed = []
    for f, checksum in zip(files, checksums):
        if file_checksum(f) != checksum:
            changed.append(f)
    return changed
