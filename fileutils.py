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


BUILD_DIR = "buildtest"

slash = "\\" if os.name == "nt" else "/"


def os_path(path):
    return path.replace("/", slash)


def net_path(path):
    return path.replace(slash, "/")


def get_contents(path):
    with open(os_path(path), "rb") as file:
        return file.read()


def write_file(path, contents):
    with open(os_path(path), "wb") as file:
        file.write(contents)


def file_checksum(path):
    return hashlib.md5(get_contents(path)).hexdigest()


def list_all_files(path = BUILD_DIR):
    all = []
    for path, dirs, files in os.walk(os_path(path)):
        for file in files:
            all.append(net_path(path) + "/" + file)
    return all


def delete_extra_files(files):
    on_disk = list_all_files(BUILD_DIR)
    for f in on_disk:
        if f not in files:
            os.remove(os_path(f))


def get_missing_files(files):
    on_disk = list_all_files()
    missing = [f for f in files if f not in on_disk]
    return missing


def verify_checksums(files, sums):
    #filters out unchanged files and returns a list of files whose checksums differ from disk
    changed = []
    for f, sum in zip(files,sums):
        if file_checksum(f) != sum:
            changed.append(f)
    return changed
