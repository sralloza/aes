import base64
from getpass import getpass
from glob import glob
from pathlib import Path
from typing import Union

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

__all__ = ["password_to_aes_key", "get_fernet", "ensure_filepath"]

path_or_str = Union[Path, str]


def password_to_aes_key(password: str):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode())
    return base64.urlsafe_b64encode(digest.finalize())


def get_fernet(password: str = None, ensure: bool = False):
    if not password:
        password = getpass("AES password: ")
        if ensure:
            password2 = getpass("Repeat password: ")

            if password != password2:
                raise ValueError("Error: passwords do not match")

    key = password_to_aes_key(password)
    return Fernet(key)


def ensure_filepath(filepath: str):
    path = _ensure_filepath(filepath)
    if path.name != Path(filepath).name:
        print("Using path %r" % path.name)
    return path


def _ensure_filepath(filepath: path_or_str):
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
