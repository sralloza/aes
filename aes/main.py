from argparse import ArgumentParser

from cryptography.fernet import InvalidToken

from aes import version
from .files import encrypt_file, decrypt_file

__all__ = ["main", "parse_args"]


def parse_args():
    parser = ArgumentParser("AES")
    parser.add_argument("--v", "-version", action="store_true", help="Show version")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    encrypt_parser = subparsers.add_parser("encrypt")
    encrypt_parser.add_argument("path", type=str)

    decrypt_parser = subparsers.add_parser("decrypt")
    decrypt_parser.add_argument("path", type=str)

    options = parser.parse_args()

    if options.command is None:
        if options.v:
            exit("Version: %r" % version)

        return parser.error("Invalid use: use decrypt or encrypt")

    return options


def main():
    options = parse_args()

    if options.v:
        exit("Version: %r" % version)

    elif options.command == "decrypt":
        try:
            decrypt_file(options.path)
        except InvalidToken:
            exit("Invalid key")
        except ValueError as err:
            exit("Error: " + err.args[0])
    elif options.command == "encrypt":
        try:
            encrypt_file(options.path)
        except InvalidToken:
            exit("Invalid key")
        except ValueError as err:
            exit("Error: " + err.args[0])
    else:
        raise ValueError("Invalid command: %r" % options.command)
