"""Manages folder encryption."""

from os import walk
from pathlib import Path
from typing import Union

from aes.files import decrypt_file, encrypt_file

_FileLike = Union[str, Path]


def encrypt_folder(folder_path: _FileLike, password: str = None):
    """Encrypts all the files within a folder.

    Args:
        folder_path (_FileLike): folder to encrypt.
        password (str, optional): password to encrypt the file. If None,
            the user will have to type it. Defaults to None.
    """

    folder_path = Path(folder_path)

    for root, _, files in walk(folder_path):
        for file in files:
            filepath = Path(root) / file
            encrypt_file(filepath, password)


def decrypt_folder(folder_path: _FileLike, password: str = None):
    """Decrypts all the files within a folder.

    Args:
        folder_path (_FileLike): folder to decrypt.
        password (str, optional): password to decrypt the file. If None,
            the user will have to type it. Defaults to None.
    """

    folder_path = Path(folder_path)

    for root, _, files in walk(folder_path):
        for file in files:
            filepath = Path(root) / file
            decrypt_file(filepath, password)
