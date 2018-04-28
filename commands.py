# Name:   Josh Wilson
# Email:  joshua.wilson@vanderbilt.edu
# Date:   15 March 2018
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: I have neither given nor received
#     unauthorized aid on this assignment.
#

import json
import shlex
import subprocess
import os
import time

TIMEOUT = 30


def run(conf_filename):
    """Runs all of the commands stored in the configuration file and stores
    their resulting return codes and textual outputs.

    If any command returns a nonzero code, no further commands are executed and
    the build is regarded as a failure. If the configuration file is not valid
    for any reason, a ValueError is raised. Commands are split with shell rules
    but are not executed in any shell.
    """
    parsed = parse_conf_file(conf_filename)
    if isinstance(parsed, str):  # describes an error that occurred
        raise ValueError(parsed)
    assert isinstance(parsed, dict)
    return execute_all(parsed["commands"])


def parse_conf_file(conf_filename):
    required_elements = ["commands"]  # extend when more json elements are required
    try:
        with open(conf_filename, "r") as conf_file:
            try:
                conf = json.load(conf_file)
            except json.decoder.JSONDecodeError:
                return "Invalid configuration file: {}: " \
                       "Decoding error".format(conf_filename)
    except FileNotFoundError:
        return "Configuration file not found: {}".format(conf_filename)

    if os.name not in conf:
        return "Platform not supported: {}".format(os.name)
    os_conf = conf[os.name]
    if any(elem not in os_conf for elem in required_elements):
        return "Invalid configuration file: {}".format(conf_filename)
    # return strings if errors, JSON object otherwise
    return os_conf


def execute_all(command_list):
    return_code = 0
    output = []
    started = time.clock()
    for command in command_list:
        # include the command itself in the output
        output.append("$ {}\n".format(command).encode("utf-8"))
        # run the command and record its return code and output
        return_code, stdout = execute_command(command)
        output.append(stdout)
        if return_code != 0:
            break
    elapsed = time.clock() - started

    if return_code == 0:
        output.append("\nCommands finished successfully in {} seconds.\n"
                      .format(round(elapsed, 6)).encode("utf-8"))
    else:
        output.append("\nCommands terminated with exit code {} in {} seconds.\n"
                      .format(return_code, round(elapsed, 6)).encode("utf-8"))
    return return_code, b"".join(output)


def execute_command(command):
    # split the command into a list using posix shell rules
    command = shlex.split(command)
    if len(command) == 0:
        return 0, b""
    try:
        # synchronously run the given command with a long timeout
        result = subprocess.run(command,
                                stdout=subprocess.PIPE,  # record output
                                stderr=subprocess.STDOUT,  # merge stderr, stdout
                                timeout=TIMEOUT)
    except FileNotFoundError:
        return 127, "{}: Command not found.\n".format(command[0].encode("utf-8"))
    except PermissionError:
        return 126, "{}: Permission denied.\n".format(command[0].encode("utf-8"))
    except subprocess.TimeoutExpired:
        # standard unix timeout exit code, message
        return 124, "{}: Timed out.\n".format(command[0]).encode("utf-8")
    except Exception:
        return 1, "{}: Unknown error.\n".format(command[0]).encode("utf-8")

    return result.returncode, result.stdout  # returncode 0 on success
