import pytest

from aes.exceptions import BaseAESError, IncorrectPasswordError


def test_base_aes_error():
    with pytest.raises(BaseAESError):
        raise BaseAESError

    assert issubclass(BaseAESError, Exception)


def test_incorrect_password_error():
    with pytest.raises(IncorrectPasswordError):
        raise IncorrectPasswordError

    assert issubclass(IncorrectPasswordError, BaseAESError)
