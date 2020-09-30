"""Module to manage the command line execution."""

import sys

import click
from cryptography.fernet import InvalidToken

from . import __version__
from .general import decrypt_from_path, encrypt_from_path, temp_decrypt

# pylint: disable=missing-docstring

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(version=__version__)
def cli():
    pass


def wrapper(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except InvalidToken:
        click.secho("Invalid password", err=True, fg="bright_red")
        sys.exit(1)
    except ValueError as err:
        arg = err.args[0] if err.args else ""
        click.secho("Error: " + arg, err=True, fg="bright_red")
        sys.exit(1)


@cli.command("decrypt")
@click.argument("path")
def decrypt_command(path):
    return wrapper(decrypt_from_path, path)


@cli.command("encrypt")
@click.argument("path")
def encrypt_command(path):
    return wrapper(encrypt_from_path, path)




def main():
    return cli(prog_name="aes") # pylint: disable=unexpected-keyword-arg
