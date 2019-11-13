from .exceptions import BaseAESError, IncorrectPasswordError
from .files import decrypt_file, encrypt_file
from .text import decrypt_text, encrypt_text
from .utils import ensure_filepath, get_fernet, password_to_aes_key
from pathlib import Path

__all__ = [
    "BaseAESError",
    "IncorrectPasswordError",
    "decrypt_file",
    "encrypt_file",
    "main",
    "decrypt_text",
    "encrypt_text",
    "ensure_filepath",
    "get_fernet",
    "password_to_aes_key",
]


def get_version():
    return Path(__file__).with_name("VERSION").read_text()


def main():
    from .main import main as _main

    return _main()
