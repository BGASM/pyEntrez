import configargparse

import cmdline as cmd


def main() -> None:
    """Command line parsing to determine how pyEntrez should be run.

    Check if user is a new user and run functions to set up user directory.
    Determine if pyEntrez should be run in TUI or CMD mode.
    Exisiting user can set up a new workspace by passing --INIT argument.
    Version checking arg.

    Attributes:
        credentials (list): List of user credentials returned from argparse.
        args (vars): Vars/dict of all args returned from argparse.
        parse (configargparse.ArgParser): ArgParser to parse the CMD arguments.
    """
    parse, path = cmd.get_parser()
    args = parse.parse_args()
    args = vars(args)
    for key in args:
        print(f'Check{key}:{args[key]}')



if __name__ == '__main__':
    main()
