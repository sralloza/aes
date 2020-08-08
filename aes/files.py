"""Module to manage file encryption."""

from pathlib import Path
from typing import Union

from .text import decrypt_text, encrypt_text

_FileLike = Union[str, Path]


def encrypt_file(filepath: _FileLike, password: str = None):
    """Encrypts a file.

    Args:
        filepath (_FileLike): filepath of the file. It must exist.
        password (str, optional): password to encrypt the file. If None,
            the user will have to type it. Defaults to None.
    """

    path = Path(filepath)
    decrypted = path.read_bytes()
    encrypted = encrypt_text(text=decrypted, password=password)

    path.write_bytes(encrypted)


def decrypt_file(filepath: _FileLike, password: str = None):
    """Decrypts a file.

    Args:
        filepath (_FileLike): filepath of the file. It must exist.
        password (str, optional): password to decrypt the file. If None,
            the user will have to type it. Defaults to None.
    """

    path = Path(filepath)

    encrypted = path.read_bytes()
    decrypted = decrypt_text(text=encrypted, password=password)

    path.write_bytes(decrypted)
