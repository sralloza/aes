from unittest import mock

import pytest

from aes.files import decrypt_file, encrypt_file

# pylint: disable=redefined-outer-name


@pytest.fixture(params=["file.txt", "foo/file.txt", "folder/doc.pdf"])
def filepath(request):
    return request.param


@pytest.fixture(params=[None, "new-password"])
def password(request):
    return request.param


@pytest.fixture(
    params=[b"message-encrypted-1", b"message-encrypted-2", b"message-encrypted-3"]
)
def text(request):
    return request.param


class TestFileEncrypt:
    @pytest.fixture(autouse=True)
    def mocks(self):
        self.enctext_m = mock.patch("aes.files.encrypt_text").start()
        self.path_m = mock.patch("aes.files.Path").start()

        yield

        mock.patch.stopall()

    def test_encrypt(self, filepath, password, text):
        self.path_m.return_value.read_bytes.return_value = text
        encrypt_file(filepath=filepath, password=password)

        self.enctext_m.assert_called_once_with(text=text, password=password)
        self.path_m.assert_called_once_with(filepath)
        self.path_m.return_value.read_bytes.assert_called_once_with()
        self.path_m.return_value.write_bytes.assert_called_once()


class TestFileDecrypt:
    @pytest.fixture(autouse=True)
    def mocks(self):
        self.decrtext_m = mock.patch("aes.files.decrypt_text").start()
        self.path_m = mock.patch("aes.files.Path").start()

        yield

        mock.patch.stopall()

    def test_decrypt(self, filepath, password, text):
        self.path_m.return_value.read_bytes.return_value = text
        decrypt_file(filepath=filepath, password=password)

        self.decrtext_m.assert_called_once_with(text=text, password=password)
        self.path_m.assert_called_once_with(filepath)
        self.path_m.return_value.read_bytes.assert_called_once_with()
        self.path_m.return_value.write_bytes.assert_called_once()
