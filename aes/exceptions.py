__all__ = ['BaseAESError', 'IncorrectPasswordError']


class BaseAESError(Exception):
    """Base AES error."""


class IncorrectPasswordError(BaseAESError):
    """Incorrect password error"""
