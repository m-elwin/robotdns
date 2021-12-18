#!/usr/bin/env python3
"""
Manages the users that are allowed to register their IP/hostname with the dns server
"""

import argparse
import sys
import os

def do_add(args):
    """ Handle the add subcommand
        args.keyfile - the public key file
        args.host  - the host
    """
    home = os.path.expanduser("~")
    auth_fname = f"{home}/.ssh/authorized_keys"
    if os.path.exists(auth_fname):
        with open(auth_fname, "r") as auth_keys:
            keys = auth_keys.readlines()
            for line in keys:
                vals = keys.split(" ")
                if vals[-1] == args.host:
                    print(f"Host {args.host} already registered and must be removed if you would like to update it", file=stderr)
                    sys.exit(1)

    with open(args.keyfile, "r") as keyfile:
        key = keyfile.readlines()
        # perform some very basic validation
        if len(key) != 1:
            print(f"Keyfile {args.keyfile} is invalid")
            sys.exit(1)
        fields = key[0].split(" ")

        if fields[0] not in ["ssh-rsa", "ssh-ed25519"]:
            print(f"Keyfile is of type {fields[0]}, which is unsupported.")
            sys.exit(1)

        with open(auth_fname, "a") as auth_keys:
            auth_keys.write(f'restrict,command="~/robotdns/robotdns/dns_update.py {args.host}" {fields[0]} {fields[1]} {args.host}')

def do_rm(args):
    """ Handle the rm subcommand
        args.host - the host to remove
    """
    # Make the changes in a new file, in case we get interrupted, then copy it over
    with open("~/.ssh/authorized_keys", "r") as auth_keys:
        keys = auth_keys.readlines()
        with open("~/.ssh/authorized_keys.new", "w") as auth_keys_new:
            for line in keys:
                vals = keys.split(" ")
                if vals[-1] != args.host:
                    auth_keys_new.write(line)

    os.replace(src="~/.ssh/authorized_keys.new", dst="~/.ssh/authorized_keys")

    
    
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

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    # Dispatch to the appropriate argument handling function
    args.func(args)
    
if __name__ == "__main__":
    main()
