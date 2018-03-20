# Name:   Josh Wilson
# Email:  joshua.wilson@vanderbilt.edu
# Date:   15 March 2018
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: I have neither given nor received
#     unauthorized aid on this assignment.

import argparse


def main():
    parse()


# Interpret the command line arguments and offer help to the user.
# True if this is a client
def parse():
    # ensure the command line arguments are correct and place them in console_args
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("mode", choices=["client", "server"], default="client", metavar="mode",
                        help="either \"client\" (send a job) or \"server\" (receive jobs)")
    console_args = parser.parse_args()

    # place the parsed data into a tuple and return it
    # ............
    return console_args.mode == "client"


def run_server():
    pass



def run_client():
    connect_to_server()
    authenticate_client()




def connect_to_server():
    pass



def authenticate_client():
    pass





# run the "main" function
if __name__ == "__main__":
    main()