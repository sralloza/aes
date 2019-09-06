from unittest import mock

import pytest

from aes.files import encrypt_file, decrypt_file


@pytest.fixture(params=['file.txt', 'foo/file.txt', 'folder/doc.pdf'])
def filepath(request):
    return request.param


@pytest.fixture(params=[None, 'new-password'])
def password(request):
    return request.param


@pytest.fixture(params=[b'message-encrypted-1', b'message-encrypted-2', b'message-encrypted-3'])
def text(request):
    return request.param

class TestFileEncrypt:
    @pytest.fixture
    def mocks(self):
        ensure_filepath_mock = mock.patch('aes.files.ensure_filepath').start()
        encrypt_text_mock = mock.patch('aes.files.encrypt_text').start()

        yield ensure_filepath_mock, encrypt_text_mock

        mock.patch.stopall()

    def test_encrypt(self, filepath, password, text, mocks):
        ensure_filepath_mock, encrypt_text_mock = mocks
        ensure_filepath_mock.return_value.read_bytes.return_value = text
        encrypt_file(filepath=filepath, password=password)

        encrypt_text_mock.assert_called_once_with(text=text, password=password)
        ensure_filepath_mock.assert_called_once_with(filepath)
        ensure_filepath_mock.return_value.read_bytes.assert_called_once_with()
        ensure_filepath_mock.return_value.write_bytes.assert_called_once()


class TestFileDecrypt:
    @pytest.fixture
    def mocks(self):
        ensure_filepath_mock = mock.patch('aes.files.ensure_filepath').start()
        decrypt_text_mock = mock.patch('aes.files.decrypt_text').start()

        yield ensure_filepath_mock, decrypt_text_mock

        mock.patch.stopall()


    def test_decrypt(self, filepath, password, text, mocks):
        ensure_filepath_mock, decrypt_text_mock = mocks
        ensure_filepath_mock.return_value.read_bytes.return_value = text
        decrypt_file(filepath=filepath, password=password)

        decrypt_text_mock.assert_called_once_with(text=text, password=password)
        ensure_filepath_mock.assert_called_once_with(filepath)
        ensure_filepath_mock.return_value.read_bytes.assert_called_once_with()
        ensure_filepath_mock.return_value.write_bytes.assert_called_once()
