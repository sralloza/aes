"""Module to manage file encryption."""

from aes.text import encrypt_text, decrypt_text
from aes.utils import ensure_filepath


def encrypt_file(filepath: str, password: str = None):
    """Encrypts a file.

    Args:
        filepath (str): filepath of the file.
        password (str, optional): password to encrypt the file. If None,
            the user will have to type it. Defaults to None.
    """

    path = ensure_filepath(filepath)

    decrypted = path.read_bytes()
    encrypted = encrypt_text(text=decrypted, password=password)

    path.write_bytes(encrypted)


def decrypt_file(filepath: str, password: str = None):
    """Decrypts a file.

    Args:
        filepath (str): filepath of the file.
        password (str, optional): password to decrypt the file. If None,
            the user will have to type it. Defaults to None.
    """

    path = ensure_filepath(filepath)

    encrypted = path.read_bytes()
    decrypted = decrypt_text(text=encrypted, password=password)

    path.write_bytes(decrypted)
