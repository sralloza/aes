"""Exceptions used in this module."""

import click


class BaseAESError(click.ClickException):
    """Base AES error."""


class FilepathError(BaseAESError):
    """Filepath error"""


class FolderNotFoundError(BaseAESError):
    """Folder not found error"""


class IncorrectPasswordError(BaseAESError):
    """Incorrect password error"""


class PasswordsMismatchError(BaseAESError):
    """Passwords mismatch error."""
