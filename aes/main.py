"""Module to manage the command line execution."""

from argparse import ArgumentParser
import sys
from typing import NoReturn

from cryptography.fernet import InvalidToken

from . import __version__
from .general import decrypt_from_path, encrypt_from_path


class Parser:
    """Represents the argument parser."""

    parser = ArgumentParser("test")

    @classmethod
    def error(cls, msg: str) -> NoReturn:
        """Prints the error message to the stderr with the program
        ussage and then exits.

        Args:
            msg (str): error message.
        """

        cls.parser.error(msg)

    @classmethod
    def parse_args(cls) -> dict:
        """Parses command line arguments.

        Returns:
            dict: arguments parsed.
        """

        cls.parser = ArgumentParser("AES")
        cls.parser.add_argument(
            "--v", "-version", action="store_true", help="Show version", dest="version"
        )
        subparsers = cls.parser.add_subparsers(title="commands", dest="command")

        encrypt_parser = subparsers.add_parser("encrypt")
        encrypt_parser.add_argument("path", type=str)

        decrypt_parser = subparsers.add_parser("decrypt")
        decrypt_parser.add_argument("path", type=str)

        options = cls.parser.parse_args()

        return vars(options)


def main():
    """Main function.

    Raises:
        ValueError: if `Parser.parse_args` returns an invalid command.

    Returns:
        None: None is always returned.

    """

    options = Parser.parse_args()

    if options["version"]:
        print("Version: %r" % __version__)
        sys.exit(0)

    if options["command"] == "decrypt":
        try:
            return decrypt_from_path(options["path"])
        except InvalidToken:
            print("Invalid password", file=sys.stderr)
            sys.exit(1)
        except ValueError as err:
            arg = err.args[0] if err.args else ""
            print("Error: " + arg, file=sys.stderr)
            sys.exit(1)
    if options["command"] == "encrypt":
        try:
            return encrypt_from_path(options["path"])
        except InvalidToken:
            print("Invalid password", file=sys.stderr)
            sys.exit(1)
        except ValueError as err:
            arg = err.args[0] if err.args else ""
            print("Error: " + arg, file=sys.stderr)
            sys.exit(1)

    msg = f"{options['command']!r} is not a valid command"
    raise ValueError(msg)
