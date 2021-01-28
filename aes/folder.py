"""Manages folder encryption."""

from os import walk
from pathlib import Path
from typing import Union

from .files import decrypt_file, encrypt_file
from .utils import check_write_access

_FileLike = Union[str, Path]


def encrypt_folder(folder_path: _FileLike, password: str = None):
    """Encrypts all the files within a folder.

    Args:
        folder_path (_FileLike): folder to encrypt.
        password (str, optional): password to encrypt the file. If None,
            the user will have to type it. Defaults to None.
    """

    folder_path = Path(folder_path)
    files_to_encrypt = []

    for root, _, files in walk(folder_path):
        for file in files:
            filepath = Path(root) / file
            check_write_access(filepath)
            files_to_encrypt.append(filepath)

    for file in files_to_encrypt:
        encrypt_file(file, password)


def decrypt_folder(folder_path: _FileLike, password: str = None):
    """Decrypts all the files within a folder.

    Args:
        folder_path (_FileLike): folder to decrypt.
        password (str, optional): password to decrypt the file. If None,
            the user will have to type it. Defaults to None.
    """

    folder_path = Path(folder_path)
    files_to_decrypt = []

    for root, _, files in walk(folder_path):
        for file in files:
            filepath = Path(root) / file
            check_write_access(filepath)
            files_to_decrypt.append(filepath)

    for file in files_to_decrypt:
        decrypt_file(file, password)
