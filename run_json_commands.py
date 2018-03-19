# Name:   Josh Wilson
# Email:  joshua.wilson@vanderbilt.edu
# Date:   15 March 2018
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: I have neither given nor received
#     unauthorized aid on this assignment.
#

import json
import subprocess

# printing all information to stdout is fine, we can redirect that
# through a socket later


def main():
    conf = parse_conf_file("buildbox.json")
    if conf is None:
        return 1
    return_code = execute_all(conf["commands"])
    if return_code == 0:
        print("Commands executed successfully.")
    else:
        print("Commands terminated with exit code {}.".format(return_code))


def parse_conf_file(conf_filename):
    # extend this when more json elements are required
    required_elements = ["commands"]

    with open(conf_filename) as conf_file:
        try:
            conf = json.load(conf_file)
        except json.decoder.JSONDecodeError:
            print("Invalid configuration file: {}: "
                  "Decoding error".format(conf_filename))
            return None
    for elem in required_elements:
        if elem not in conf:
            print("Invalid configuration file: {}: "
                  "Does not contain {}".format(conf_filename, elem))
            return None
    return conf


def execute_all(command_list):
    for command in command_list:
        return_code = execute_command(command)
        if return_code != 0:
            return return_code
    return 0


def execute_command(command):
    try:
        # synchronously run the given command in a shell with a 30 second timeout
        result = subprocess.run(command, shell=True, stderr=subprocess.STDOUT, timeout=30)
    except subprocess.TimeoutExpired:
        print("Bad command: {}: "
              "Timed out".format(command))
        return 124  # standard unix timeout exit code
    return result.returncode  # 0 on success


# run the "main" function
if __name__ == "__main__":
    main()