"""Useful functions for the hole module."""

import base64
from functools import lru_cache
from getpass import getpass
from glob import glob
from pathlib import Path
from typing import Union

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

_FileLike = Union[Path, str]


def password_to_aes_key(password: str) -> bytes:
    """Transforms a simple str password into an AES key.

    Args:
        password (str): password.

    Returns:
        bytes: AES key generated from the password.
    """

    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode())
    return base64.urlsafe_b64encode(digest.finalize())


@lru_cache(maxsize=10)
def get_fernet(password: str = None, ensure: bool = True) -> Fernet:
    """Returns a `Fernet` object to encrypt and decrypt text.

    Args:
        password (str, optional): if not given, the user will have to type it
            using the stdin. Defaults to None.
        ensure (bool, optional): if True and password is None, the user will have
            to input the password twice. Defaults to True.

    Raises:
        ValueError: If `password` is None, `ensure` is True and the two input passwords
            doesn't match.

    Returns:
        Fernet: `Fernet` object to encrypt and decrypt text.
    """

    if not password:
        password = getpass("AES password: ")
        if ensure:
            password2 = getpass("Repeat password: ")

            if password != password2:
                raise ValueError("Error: passwords do not match")

    key = password_to_aes_key(password)
    return Fernet(key)


def ensure_filepath(filepath: _FileLike) -> Path:
    """Wrapper for `_ensure_filepath`. If the filepath detected is not the same as
    the `filepath` argument, a warning will be printed to stdout.

    Args:
        filepath (_FileLike): filepath.

    Returns:
        Path: ensured filepath.
    """

    path = _ensure_filepath(filepath)
    if path.name != Path(filepath).name:
        print("Using path %r" % path.name)
    return path


def _ensure_filepath(filepath: _FileLike) -> Path:
    """Ensures a filepath. If the filepath exists, that filepath is returned.
    However if it doesn't exist, this function will try to find a file using
    the `*` glob pattern.

    Args:
        filepath (_FileLike): filepath to start the search.

    Raises:
        ValueError: if `filepath` doesn't exist and no file is found using
            the glob pattern.

    Returns:
        Path: path of the selected file.
    """

    path = Path(filepath).absolute()
    if not path.exists():
        # If the file does not exist, find it using glob.
        possible = glob(path.with_name(path.name + "*").as_posix())

        if len(possible) == 1:
            return Path(possible[0])
        possible = glob(path.with_name("*" + path.name).as_posix())

        if len(possible) == 1:
            return Path(possible[0])
        possible = glob(path.with_name("*" + path.name + "*").as_posix())

        if len(possible) == 1:
            return Path(possible[0])

        raise ValueError("Invalid filepath: %s" % filepath)
    return path
