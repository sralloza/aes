from unittest import mock

import pytest

from aes import IncorrectPasswordError, decrypt_text, encrypt_text


class TestTextEncrypt:
    texts = [
        "test-1",
        "9813265",
        '897*^(/&"%/$(=!',
        'YC(/KCD)(&/")/"$=)FIKJC',
        b"test-1",
        b"9813265",
        b'897*^(/&"%/$(=!',
        b'YC(/KCD)(&/")/"$=)FIKJC',
    ]

    @pytest.fixture(params=texts)
    def text(self, request):
        return request.param

    @pytest.fixture(params=[None, "new-password"])
    def password(self, request):
        return request.param

    @mock.patch("aes.text.get_fernet")
    def test_text_encrypt(self, get_fernet_mock, text, password):
        encrypt_text(text=text, password=password)

        if isinstance(text, str):
            text = text.encode()

        get_fernet_mock.assert_called_once_with(ensure=True, password=password)
        get_fernet_mock.return_value.encrypt.assert_called_with(text)


class TestTextDecrypt:
    texts = [
        "test-1",
        "9813265",
        '897*^(/&"%/$(=!',
        'YC(/KCD)(&/")/"$=)FIKJC',
        b"test-1",
        b"9813265",
        b'897*^(/&"%/$(=!',
        b'YC(/KCD)(&/")/"$=)FIKJC',
    ]

    @pytest.fixture(params=texts)
    def text(self, request):
        return request.param

    @pytest.fixture(params=[None, "new-password"])
    def password(self, request):
        return request.param

    @mock.patch("aes.text.get_fernet")
    def test_text_encrypt(self, get_fernet_mock, text, password):
        decrypt_text(text=text, password=password)

        if isinstance(text, str):
            text = text.encode()

        get_fernet_mock.assert_called_once_with(ensure=False, password=password)
        get_fernet_mock.return_value.decrypt.assert_called_with(text)

    @mock.patch("aes.text.get_fernet")
    def test_text_encrypt_error(self, get_fernet_mock, text, password):
        with pytest.raises(IncorrectPasswordError):
            decrypt_text(text=text, password=password)

        if isinstance(text, str):
            text = text.encode()

        get_fernet_mock.assert_called_once_with(ensure=False, password=password)
        get_fernet_mock.return_value.decrypt.assert_called_with(text)
