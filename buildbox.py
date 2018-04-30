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
        if console_args.dry_run:
            console_args.no_build = True  # --dry-run implies --no-build
        import client
        return client.run(console_args)
    else:
        import server
        return server.run(console_args)


def parse():
    """Interpret the command line arguments and offer help to the user.

    The mode field of the returned object is either "client" or "server".
    """
    parser = argparse.ArgumentParser(add_help=True)
    subparsers = parser.add_subparsers(title="modes", dest="mode")

    client_parser = subparsers.add_parser("client")
    client_parser.add_argument("host", help="the host running buildbox in server mode")
    client_parser.add_argument("-r", "--root", default=".",
                               help="the directory to synchronize")
    client_parser.add_argument("-q", "--quiet", action="store_true",
                               help="suppress output information")
    client_parser.add_argument("-d", "--dry-run", action="store_true",
                               help="do not alter the server's state")
    client_parser.add_argument("-n", "--no-build", action="store_true",
                               help="synchronize files but do not run commands")

    server_parser = subparsers.add_parser("server")
    server_parser.add_argument("-q", "--quiet", action="store_true",
                               help="suppress output information")
    server_parser.add_argument("-f", "--file", default="buildbox.json",
                               help="the JSON config file to use (default buildbox.json)")

    return parser.parse_args()


# run the "main" function
if __name__ == "__main__":
    main()
