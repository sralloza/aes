"""Manages text encription."""

from typing import Union

from cryptography.fernet import InvalidToken

from aes.exceptions import IncorrectPasswordError
from aes.utils import get_fernet

StrOrBytes = Union[str, bytes]


def encrypt_text(text: StrOrBytes, password: str = None) -> bytes:
    """Encrypts text.

    Args:
        text (StrOrBytes): text to encrypt.
        password (str, optional): password to encrypt the file. If None,
            the user will have to type it. Defaults to None.

    Returns:
        bytes: text encrypted.
    """

    fernet = get_fernet(password=password, ensure=True)

    if isinstance(text, str):
        text = text.encode()

    return fernet.encrypt(text)


def decrypt_text(text: StrOrBytes, password: str = None) -> bytes:
    """Decrypts text.

    Args:
        text (StrOrBytes): text to decrypt.
        password (str, optional): password to decrypt the file. If None,
            the user will have to type it. Defaults to None.

    Raises:
        IncorrectPasswordError: if the AES algorithm doesn't work due
            to an incorrect password.

    Returns:
        bytes: text decrypted.
    """

    fernet = get_fernet(password=password, ensure=False)

    if isinstance(text, str):
        text = text.encode()

    try:
        return fernet.decrypt(text)
    except InvalidToken as exc:
        raise IncorrectPasswordError from exc
