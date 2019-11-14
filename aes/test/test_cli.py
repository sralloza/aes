from unittest import mock

import pytest
from cryptography.fernet import InvalidToken

from aes import main
from aes.cli import parse_args


class TestParseArgs:
    def parse_args(self, *args):
        return vars(parse_args(*args))

    def test_version(self):
        args1 = self.parse_args("-v")
        assert args1["command"] is None
        assert args1["version"] is True
        assert "path" not in args1

        args2 = self.parse_args("-v", "encrypt", "path")
        assert args2["command"] == "encrypt"
        assert args2["version"] is True
        assert "path" in args2

        args3 = self.parse_args("-v", "decrypt", "path")
        assert args3["command"] == "decrypt"
        assert args3["version"] is True
        assert "path" in args3

        args4 = self.parse_args("encrypt", "path")
        assert args4["command"] == "encrypt"
        assert args4["version"] is False
        assert "path" in args4

    def test_encrypt(self, capsys):
        args = self.parse_args("encrypt", "file-path")
        assert args["command"] == "encrypt"
        assert args["path"] == "file-path"

        with pytest.raises(SystemExit):
            self.parse_args("encrypt")

        captured = capsys.readouterr()
        assert "the following arguments are required: path" in captured.err

    def test_decrypt(self, capsys):
        args = self.parse_args("decrypt", "file-path")
        assert args["command"] == "decrypt"
        assert args["path"] == "file-path"

        with pytest.raises(SystemExit):
            self.parse_args("decrypt")

        captured = capsys.readouterr()
        assert "the following arguments are required: path" in captured.err

    def test_emtpy(self, capsys):
        with pytest.raises(SystemExit):
            self.parse_args()
        captured = capsys.readouterr()
        assert "Invalid use" in captured.err


class TestMain:
    def test_version(self):
        with pytest.raises(SystemExit, match="Version:"):
            main("--v")

    @mock.patch("aes.cli.encrypt_file")
    def test_encrypt_file_good(self, encrypt_mock):
        main("encrypt", "filepath")
        encrypt_mock.assert_called_once_with("filepath")

    @mock.patch("aes.cli.encrypt_file")
    def test_encrypt_file_encryption_error(self, encrypt_mock):
        encrypt_mock.side_effect = InvalidToken

        with pytest.raises(SystemExit, match="Invalid password"):
            main("encrypt", "filepath")
        encrypt_mock.assert_called_once_with("filepath")

    @mock.patch("aes.cli.encrypt_file")
    def test_encrypt_file_value_error(self, encrypt_mock):
        encrypt_mock.side_effect = ValueError

        with pytest.raises(SystemExit, match="Error:"):
            main("encrypt", "filepath")
        encrypt_mock.assert_called_once_with("filepath")

    @mock.patch("aes.cli.decrypt_file")
    def test_decrypt_file_good(self, decrypt_mock):
        main("decrypt", "filepath")
        decrypt_mock.assert_called_once_with("filepath")

    @mock.patch("aes.cli.decrypt_file")
    def test_decrypt_file_decryption_error(self, decrypt_mock):
        decrypt_mock.side_effect = InvalidToken

        with pytest.raises(SystemExit, match="Invalid password"):
            main("decrypt", "filepath")
        decrypt_mock.assert_called_once_with("filepath")

    @mock.patch("aes.cli.decrypt_file")
    def test_decrypt_file_value_error(self, decrypt_mock):
        decrypt_mock.side_effect = ValueError

        with pytest.raises(SystemExit, match="Error:"):
            main("decrypt", "filepath")
        decrypt_mock.assert_called_once_with("filepath")
