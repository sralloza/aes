__all__ = ["BaseAESError", "IncorrectPasswordError"]


class BaseAESError(Exception):
    """Base AES error."""


class FolderNotFoundError(BaseAESError):
    """Folder not found error"""


class IncorrectPasswordError(BaseAESError):
    """Incorrect password error"""
