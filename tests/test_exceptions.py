from click.exceptions import ClickException
import pytest

from aes.exceptions import (
    BaseAESError,
    FilepathError,
    IncorrectPasswordError,
    PasswordsMismatchError,
)


class TestBaseAesError:
    def test_inheritance(self):
        assert issubclass(BaseAESError, ClickException)

    def test_raise(self):
        with pytest.raises(BaseAESError):
            raise BaseAESError("message")


class TestIncorrectPasswordError:
    def test_inheritance(self):
        assert issubclass(IncorrectPasswordError, BaseAESError)

    def test_raise(self):
        with pytest.raises(IncorrectPasswordError):
            raise IncorrectPasswordError("message")


class TestFilepathError:
    def test_inheritance(self):
        assert issubclass(FilepathError, BaseAESError)

    def test_raise(self):
        with pytest.raises(FilepathError):
            raise FilepathError("message")


class TestPasswordsMismatchError:
    def test_inheritance(self):
        assert issubclass(PasswordsMismatchError, BaseAESError)

    def test_raise(self):
        with pytest.raises(PasswordsMismatchError):
            raise PasswordsMismatchError("message")
