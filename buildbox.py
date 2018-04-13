# Name:   Josh Wilson, Jerry Jung, Caleb Proffitt
# Date:   <DATE>
# Course: CS 4283 - Vanderbilt University
# Ver:    Python 3.6.4
# Honor statement: We have neither given nor received
#     unauthorized aid on this assignment.

import argparse


def main():
    console_args = parse()
    if console_args.mode == "client":
        import client
        return client.run(console_args.host)
    else:
        import server
        return server.run()


def parse():
    """Interpret the command line arguments and offer help to the user.

    True if this is a client, false if this is a server.
    """
    # ensure the command line arguments are correct and place them in console_args
    parser = argparse.ArgumentParser(add_help=True)
    subparsers = parser.add_subparsers(title="modes", dest="mode")
    client_parser = subparsers.add_parser("client")
    client_parser.add_argument("host", help="the host running buildbox in server mode")
    server_parser = subparsers.add_parser("server")
    return parser.parse_args()


# run the "main" function
if __name__ == "__main__":
    main()
