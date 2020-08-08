"""General encryption manager."""

from pathlib import Path

from .files import decrypt_file, encrypt_file
from .folder import decrypt_folder, encrypt_folder
from .utils import ensure_filepath


def encrypt_from_path(input_path: str, password: str = None):
    """Encrypts files given a pattern.

    Args:
        input_path (str): pattern to encrypt. Can be a folder too.
        password (str, optional): password to encrypt the file. If None,
            the user will have to type it. Defaults to None.

    Returns:
        None: None is always returned.
    """

    path = Path(input_path)
    if path.is_dir():
        return encrypt_folder(path, password)

    filepath = ensure_filepath(path)
    return encrypt_file(filepath, password)


def decrypt_from_path(input_path: str, password: str = None):
    """Encrypts files given a pattern.

    Args:
        input_path (str): pattern to encrypt. Can be a folder too.
        password (str, optional): password to encrypt the file. If None,
            the user will have to type it. Defaults to None.

    Returns:
        None: None is always returned.
    """

    path = Path(input_path)
    if path.is_dir():
        return decrypt_folder(path, password)

    filepath = ensure_filepath(path)
    return decrypt_file(filepath, password)
