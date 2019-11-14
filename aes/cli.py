from argparse import ArgumentParser

from cryptography.fernet import InvalidToken

from . import get_version
from .files import decrypt_file, encrypt_file

__all__ = ["main", "parse_args"]


def parse_args(*args):
    parser = ArgumentParser("AES")
    parser.add_argument(
        "--v", "-version", action="store_true", help="Show version", dest="version"
    )
    subparsers = parser.add_subparsers(title="commands", dest="command")

    encrypt_parser = subparsers.add_parser("encrypt")
    encrypt_parser.add_argument("path", type=str)

    decrypt_parser = subparsers.add_parser("decrypt")
    decrypt_parser.add_argument("path", type=str)

    options = parser.parse_args(args)

    if options.command is None:
        if not options.version:
            return parser.error("Invalid use: use decrypt or encrypt")

    return options


def main(*args):
    options = parse_args(*args)

    if options.version:
        exit("Version: %r" % get_version())

    elif options.command == "decrypt":
        try:
            decrypt_file(options.path)
        except InvalidToken:
            exit("Invalid password")
        except ValueError as err:
            arg = err.args[0] if err.args else ""
            exit("Error: " + arg)
    elif options.command == "encrypt":
        try:
            encrypt_file(options.path)
        except InvalidToken:
            exit("Invalid password")
        except ValueError as err:
            arg = err.args[0] if err.args else ""
            exit("Error: " + arg)
