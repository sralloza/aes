import base64
from getpass import getpass
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

__all__ = ['encrypt', 'decrypt', 'password_to_aes_key', 'get_fernet', 'ensure_filepath']


def encrypt(filepath: str):
    path = ensure_filepath(filepath)
    fernet = get_fernet(ensure=True)

    decrypted = path.read_bytes()
    encrypted = fernet.encrypt(decrypted)

    path.write_bytes(encrypted)


def decrypt(filepath: str):
    path = ensure_filepath(filepath)
    fernet = get_fernet()

    encrypted = path.read_bytes()
    decrypted = fernet.decrypt(encrypted)

    path.write_bytes(decrypted)


def password_to_aes_key(password: str):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode())
    return base64.urlsafe_b64encode(digest.finalize())


def get_fernet(password=None, ensure=False):
    if not password:
        password = getpass('AES password: ')
        if ensure:
            password2 = getpass('Repeat password: ')

            if password != password2:
                raise ValueError('Error: passwords do not match')

    key = password_to_aes_key(password)
    return Fernet(key)


def ensure_filepath(filepath: str):
    path = _ensure_filepath(filepath)
    if path.name != Path(filepath).name:
        print('Using path %r' % path.name)
    return path


def _ensure_filepath(filepath: str):
    path = Path(filepath).absolute()
    if not path.exists():
        possible = list(path.parent.glob(filepath))

        if len(possible) == 1:
            return possible[0]
        possible = list(path.parent.glob(filepath + '*'))

        if len(possible) == 1:
            return possible[0]
        possible = list(path.parent.glob('*' + filepath))

        if len(possible) == 1:
            return possible[0]
        possible = list(path.parent.glob('*' + filepath + '*'))

        if len(possible) == 1:
            return possible[0]

        raise ValueError('Invalid filepath: %s' % filepath)
    return path
