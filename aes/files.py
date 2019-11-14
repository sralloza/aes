from aes.text import encrypt_text, decrypt_text
from aes.utils import ensure_filepath

__all__ = ["encrypt_file", "decrypt_file"]


def encrypt_file(filepath: str, password: str = None):
    path = ensure_filepath(filepath)

    decrypted = path.read_bytes()
    encrypted = encrypt_text(text=decrypted, password=password)

    path.write_bytes(encrypted)


def decrypt_file(filepath: str, password: str = None):
    path = ensure_filepath(filepath)

    encrypted = path.read_bytes()
    decrypted = decrypt_text(text=encrypted, password=password)

    path.write_bytes(decrypted)
