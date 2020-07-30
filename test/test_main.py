import argparse
from argparse import Namespace
from os.path import realpath
import shlex
from unittest import mock

import pytest
from cryptography.fernet import InvalidToken

from aes.main import main, Parser


class TestParseArgs:
    @mock.patch("sys.argv")
    def set_args(self, string="", sys_argv_m=None):
        # breakpoint()
        real_args = ["test.py"] + shlex.split(string)
        sys_argv_m.__getitem__.side_effect = lambda s: real_args[s]
        try:
            args = Parser.parse_args()
            return args
        finally:
            sys_argv_m.__getitem__.assert_called_once_with(slice(1, None, None))

    def test_version(self):
        args1 = self.set_args("-v")
        assert args1["command"] is None
        assert args1["version"] is True
        assert "path" not in args1

        args2 = self.set_args("-v encrypt path")
        assert args2["command"] == "encrypt"
        assert args2["version"] is True
        assert "path" in args2

        args3 = self.set_args("-v decrypt path")
        assert args3["command"] == "decrypt"
        assert args3["version"] is True
        assert "path" in args3

        args4 = self.set_args("encrypt path")
        assert args4["command"] == "encrypt"
        assert args4["version"] is False
        assert "path" in args4

    def test_encrypt(self, capsys):
        args = self.set_args("encrypt file-path")
        assert args["command"] == "encrypt"
        assert args["path"] == "file-path"

        with pytest.raises(SystemExit):
            self.set_args("encrypt")

        captured = capsys.readouterr()
        assert captured.out == ""
        assert "the following arguments are required: path" in captured.err

    def test_decrypt(self, capsys):
        args = self.set_args("decrypt file-path")
        assert args["command"] == "decrypt"
        assert args["path"] == "file-path"

        with pytest.raises(SystemExit):
            self.set_args("decrypt")

        captured = capsys.readouterr()
        assert "the following arguments are required: path" in captured.err
        assert captured.out == ""

    def test_emtpy(self, capsys):
        self.set_args("")
        captured = capsys.readouterr()
        assert captured.err == ""
        assert captured.out == ""


class TestMain:
    @pytest.fixture(autouse=True)
    def mocks(self):
        self.parse_args_m = mock.patch("aes.main.Parser.parse_args").start()
        yield
        mock.patch.stopall()

    def set_args(self, **kwargs):
        real_kwargs = {"command": None, "version": False}
        real_kwargs.update(kwargs)
        self.parse_args_m.return_value = real_kwargs

    @mock.patch("aes.main.encrypt_file")
    def test_encrypt_file_good(self, encrypt_mock):
        self.set_args(command="encrypt", path="filepath")
        main()
        encrypt_mock.assert_called_once_with("filepath")

    @mock.patch("aes.main.encrypt_file")
    def test_encrypt_file_encryption_error(self, encrypt_mock):
        encrypt_mock.side_effect = InvalidToken

        with pytest.raises(SystemExit, match="Invalid password"):
            self.set_args(command="encrypt", path="filepath")
            main()
        encrypt_mock.assert_called_once_with("filepath")

    @mock.patch("aes.main.encrypt_file")
    def test_encrypt_file_value_error(self, encrypt_mock):
        encrypt_mock.side_effect = ValueError

        with pytest.raises(SystemExit, match="Error:"):
            self.set_args(command="encrypt", path="filepath")
            main()
        encrypt_mock.assert_called_once_with("filepath")

    @mock.patch("aes.main.decrypt_file")
    def test_decrypt_file_good(self, decrypt_mock):
        self.set_args(command="decrypt", path="filepath")
        main()
        decrypt_mock.assert_called_once_with("filepath")

    @mock.patch("aes.main.decrypt_file")
    def test_decrypt_file_decryption_error(self, decrypt_mock):
        decrypt_mock.side_effect = InvalidToken

        with pytest.raises(SystemExit, match="Invalid password"):
            self.set_args(command="decrypt", path="filepath")
            main()
        decrypt_mock.assert_called_once_with("filepath")

    @mock.patch("aes.main.decrypt_file")
    def test_decrypt_file_value_error(self, decrypt_mock):
        decrypt_mock.side_effect = ValueError

        with pytest.raises(SystemExit, match="Error:"):
            self.set_args(command="decrypt", path="filepath")
            main()
        decrypt_mock.assert_called_once_with("filepath")
