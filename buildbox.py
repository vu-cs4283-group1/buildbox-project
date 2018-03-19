# Name:   Josh Wilson
# Email:  joshua.wilson@vanderbilt.edu
# Date:   15 March 2018
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: I have neither given nor received
#     unauthorized aid on this assignment.

import argparse


def main():
    pass


# Interpret the command line arguments and offer help to the user.
# Returns the tuple (method, host, path, port)
def parse():
    # ensure the command line arguments are correct and place them in console_args
    parser = argparse.ArgumentParser()
    parser.add_argument("--server",
                        help="run in server mode")
    parser.add_argument("--client",
                        help="the type of HTTP request to be sent, either \"GET\" or \"HEAD\"")
    parser.add_mutually_exclusive_group()
    console_args = parser.parse_args()

    # place the parsed data into a tuple and return it
    #............
    return


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