from typing import Union

from cryptography.fernet import InvalidToken

from aes.exceptions import IncorrectPasswordError
from aes.utils import get_fernet

str_or_bytes = Union[str, bytes]

__all__ = ['encrypt_text', 'decrypt_text']


def encrypt_text(text: str_or_bytes, password: str = None):
    fernet = get_fernet(password=password, ensure=True)

    if isinstance(text, str):
        text = text.encode()

    return fernet.encrypt(text)


def decrypt_text(text: str_or_bytes, password: str = None):
    fernet = get_fernet(password=password, ensure=False)

    if isinstance(text, str):
        text = text.encode()

    try:
        return fernet.decrypt(text)
    except InvalidToken:
        raise IncorrectPasswordError
