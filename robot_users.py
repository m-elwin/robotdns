#!/usr/bin/env python3
"""
Manages the users that are allowed to register their IP/hostname with the dns server
"""

import argparse
import sys

def do_add(args):
    """ Handle the add subcommand
        args.keyfile - the public key file
        args.host  - the host
    """
    print("do_add")

def do_rm(args):
    """ Handle the rm subcommand
        args.host - the host to remove
    """
    print("do_rm")
    
def main():
    parser = argparse.ArgumentParser(description="Manage users that are allowed to register their IP/hostname")
    subparsers = parser.add_subparsers(help="Possible sub commands")

    parser_add = subparsers.add_parser('add', help='Add a user')
    parser_add.add_argument('keyfile', type=str, help="The public key file")
    parser_add.add_argument('host', type=str, help="The hostname of the user")
    parser_add.set_defaults(func=do_add)
    
    parser_rm = subparsers.add_parser('rm', help='Remove a user')
    parser_rm.add_argument('host', type=str, help="Hostname of the user to remove")
    parser_rm.set_defaults(func=do_rm)

    # If only a subcommand or no commands is passed, help is displayed
    args = parser.parse_args(args=None if sys.argv[2:] else ['--help'])

    # Dispatch to the appropriate argument handling function
    args.func(args)
    
if __name__ == "__main__":
    main()
