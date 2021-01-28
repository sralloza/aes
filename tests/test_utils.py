import base64
import functools
from pathlib import Path
from unittest import mock
from click.exceptions import ClickException

from cryptography.fernet import Fernet
import pytest

from aes.exceptions import FilepathError, PasswordsMismatchError
from aes.utils import (
    _InternalMemory,
    _ensure_filepath,
    check_write_access,
    ensure_filepath,
    get_fernet,
    password_to_aes_key,
)

# pylint: disable=redefined-outer-name,protected-access

PASSWORDS = [
    "hi",
    "hello",
    "penthagon",
    "a-fdiwkvnxoeokd",
    '12345/!"$%&/()=?¿*^¨:_;<>\\',
]
KEY = b"KKSuP8aAubHTLcnHxY8dgTHYOTeqSll6Bqs_wdXwlFA="
ROOT = Path(__file__).parent.parent.parent
FILEPATHS = [
    "file.txt",
    "images/photo.png",
    "folder/doc.pdf",
    "4.txt",
    "invalid.py",
    Path("asdf.pdf"),
    Path("a.jpg"),
]


@pytest.mark.parametrize("password", PASSWORDS)
def test_password_to_aes_key(password):
    aes_key = password_to_aes_key(password)
    assert len(aes_key) == len(Fernet.generate_key())


class TestGetFernet:
    @staticmethod
    def _fernet_to_key(fernet):
        return base64.urlsafe_b64encode(fernet._signing_key + fernet._encryption_key)

    @pytest.fixture
    def mocks(self):
        getpass_mock = mock.patch("aes.utils.getpass").start()
        ptk_mock = mock.patch("aes.utils.password_to_aes_key", return_value=KEY).start()

        assert hasattr(_InternalMemory, "saved_password")
        _InternalMemory.saved_password = None

        yield getpass_mock, ptk_mock

        mock.patch.stopall()

    @pytest.fixture(params=[None, "new-password"])
    def password(self, request):
        return request.param

    @pytest.fixture(params=[None, True])
    def ensure(self, request):
        return request.param

    @pytest.fixture(params=[True, False])
    def password_correct(self, request):
        return request.param

    def test_get_fernet(self, mocks, password, ensure, password_correct):
        get_fernet.cache_clear()
        getpass_mock, ptk_mock = mocks

        if password_correct:
            getpass_mock.return_value = "typed-password"
        else:
            getpass_mock.side_effect = ["typed-password", "wrong-password"]

        if not password_correct and ensure and not password:
            with pytest.raises(
                PasswordsMismatchError, match="Error: passwords do not match"
            ):
                get_fernet(password=password, ensure=ensure)
            return

        fernet_1 = get_fernet(password=password, ensure=ensure)
        cache_info = get_fernet.cache_info()
        assert cache_info.hits == 0
        assert cache_info.misses == 1
        assert cache_info.currsize == 1
        get_fernet.cache_clear()

        if not password:
            assert _InternalMemory.saved_password is not None

        fernet_2 = get_fernet(password=password, ensure=ensure)

        assert isinstance(fernet_1, Fernet)
        assert isinstance(fernet_2, Fernet)
        assert self._fernet_to_key(fernet_1) == KEY
        assert self._fernet_to_key(fernet_2) == KEY

        assert isinstance(get_fernet, functools._lru_cache_wrapper)

        if password:
            ptk_mock.assert_any_call("new-password")
            assert ptk_mock.call_count == 2
            getpass_mock.assert_not_called()
        else:
            ptk_mock.assert_any_call("typed-password")
            assert ptk_mock.call_count == 2
            getpass_mock.assert_called()

        if ensure and not password:
            getpass_mock.assert_called()
            assert getpass_mock.call_count == 2


@pytest.fixture(params=FILEPATHS)
def filepath(request):
    return request.param


@pytest.fixture(params=[True, False])
def is_equal(request):
    return request.param


@mock.patch("aes.utils._ensure_filepath")
@mock.patch("aes.utils.Path")
def test_ensure_filepath(hef_m, path_mock, filepath, is_equal, capsys):
    path_mock.return_value.name = filepath
    if not is_equal:
        hef_m.return_value.name = "a.txt"
    else:
        hef_m.return_value.name = filepath

    ensure_filepath(filepath)

    captured = capsys.readouterr()

    path_mock.assert_called_with(filepath)
    hef_m.assert_called_with(filepath)

    if not is_equal:
        assert captured.out == "Using path %r\n" % filepath
    else:
        assert captured.out == ""


class TestHiddenEnsureFilepath:
    @pytest.fixture
    def data_path(self):
        return Path(__file__).parent / "test_data" / "ensure_filepath"

    def test_file_exists(self, data_path):
        filepath = data_path.joinpath("1.pdf")
        assert filepath == _ensure_filepath(filepath.as_posix())

    def test_file_not_exist_layer_one(self, data_path):
        returned_filepath = _ensure_filepath(data_path.joinpath("1"))
        assert returned_filepath == data_path.joinpath("1.pdf")

    def test_file_not_exist_layer_two(self, data_path):
        returned_filepath = _ensure_filepath(data_path.joinpath("txt"))
        assert returned_filepath == data_path.joinpath("4.txt")

    def test_file_not_exist_layer_three(self, data_path):
        returned_filepath = _ensure_filepath(data_path.joinpath("17"))
        assert returned_filepath == data_path.joinpath("photo-17.jpg")

    def test_file_not_exist_fatal_error(self, data_path):
        with pytest.raises(FilepathError, match="Invalid filepath"):
            _ensure_filepath(data_path.joinpath("invalid.py"))


def test_check_write_access():
    file_1 = mock.MagicMock()
    file_1.open.side_effect = PermissionError

    with pytest.raises(ClickException):
        check_write_access(file_1)
    file_1.open.assert_called_once()

    file_2 = mock.MagicMock()

    check_write_access(file_2)
    file_2.open.assert_called_once()
