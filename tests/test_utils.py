import base64
from pathlib import Path
from unittest import mock

import pytest
from cryptography.fernet import Fernet

from aes.utils import _ensure_filepath, password_to_aes_key, get_fernet, ensure_filepath

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
        getpass_mock, ptk_mock = mocks

        if password_correct:
            getpass_mock.return_value = "typed-password"
        else:
            getpass_mock.side_effect = ["typed-password", "wrong-password"]

        if not password_correct and ensure and not password:
            with pytest.raises(ValueError, match="Error: passwords do not match"):
                get_fernet(password=password, ensure=ensure)
            return

        fernet = get_fernet(password=password, ensure=ensure)

        if password:
            ptk_mock.assert_called_once_with("new-password")
            getpass_mock.assert_not_called()
        else:
            ptk_mock.assert_called_once_with("typed-password")
            getpass_mock.assert_called()

        if ensure and not password:
            getpass_mock.assert_called()
            assert getpass_mock.call_count == 2

        assert isinstance(fernet, Fernet)
        assert self._fernet_to_key(fernet) == KEY


@pytest.fixture(
    params=["file.txt", "images/photo.png", "folder/doc.pdf", "4.txt", "invalid.py"]
)
def filepath(request):
    return request.param


@pytest.fixture(params=[True, False])
def is_equal(request):
    return request.param


@mock.patch("aes.utils._ensure_filepath")
@mock.patch("aes.utils.Path")
def test_ensure_filepath(
    hidden_ensure_filepath_mock, path_mock, filepath, is_equal, capsys
):
    path_mock.return_value.name = filepath
    if not is_equal:
        hidden_ensure_filepath_mock.return_value.name = "a.txt"
    else:
        hidden_ensure_filepath_mock.return_value.name = filepath

    ensure_filepath(filepath)

    captured = capsys.readouterr()

    path_mock.assert_called_with(filepath)
    hidden_ensure_filepath_mock.assert_called_with(filepath)

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
        with pytest.raises(ValueError, match="Invalid filepath"):
            _ensure_filepath(data_path.joinpath("invalid.py"))
