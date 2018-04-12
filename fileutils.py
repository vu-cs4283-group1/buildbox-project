# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   12 April 2018
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.
#
# Description: This file includes utility functions for interacting with the filesystem

import hashlib

def get_contents(path):
    with open(path, "rb") as file:
        return file.read()

def file_checksum(path):
    return hashlib.md5(get_contents(path)).hexdigest()

def delete_extra_files(files):
    #deletes any files in the build directory that are not in the given list
    raise NotImplemented

def get_missing_files(files):
    raise NotImplemented


def verify_checksums(files, sums):
    #filters out unchanged files and returns a list of files whose checksums differ from disk
    changed = []
    for f, sum in zip(files,sums):
        if file_checksum(f) != sum:
            changed.append(f)
    return changed
