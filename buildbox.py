# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   <DATE>
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.

import argparse
import buildbox_server

PORT = 3035  # 0xBDB, for buildbox
LISTENER_COUNT = 5


def main():
    is_client = parse()
    return run_client() if is_client else run_server()


# Interpret the command line arguments and offer help to the user.
# True if this is a client, false if this is a server
def parse() -> bool:
    # ensure the command line arguments are correct and place them in console_args
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("mode", choices=["client", "server"], default="client", metavar="mode",
                        help="either 'client' (send a job) or 'server' (receive jobs)")
    console_args = parser.parse_args()

    # place the parsed data into a tuple and return it
    # ............
    return console_args.mode == "client"






def run_client():
    connect_to_server()
    authenticate_client()


def run_server():
    server_socket = buildbox_server.setup_server(PORT, LISTENER_COUNT)
    buildbox_server.start_server(server_socket)


def connect_to_server():
    pass



def authenticate_client():
    pass





# run the "main" function
if __name__ == "__main__":
    main()