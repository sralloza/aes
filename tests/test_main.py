from unittest import mock

from click.testing import CliRunner
from cryptography.fernet import InvalidToken
import pytest

from aes import __version__
from aes.main import cli, main


@pytest.mark.parametrize("arg", ["-h", "--help"])
def test_help(arg):
    runner = CliRunner()
    result = runner.invoke(cli, [arg])

    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    assert "Options:" in result.stdout
    assert "Commands:" in result.stdout


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert result.output == "cli, version " + str(__version__) + "\n"


@mock.patch("aes.main.encrypt_from_path")
def test_encrypt_from_path_good(encrypt_m):
    runner = CliRunner()
    result = runner.invoke(cli, ["encrypt", "filepath"])

    assert result.exit_code == 0
    assert result.output == ""

    encrypt_m.assert_called_once_with("filepath")


@mock.patch("aes.main.encrypt_from_path")
def test_encrypt_from_path_encryption_error(encrypt_m):
    encrypt_m.side_effect = InvalidToken

    runner = CliRunner()
    result = runner.invoke(cli, ["encrypt", "filepath"])

    assert result.exit_code == 1
    assert "Invalid password" in result.output

    encrypt_m.assert_called_once_with("filepath")


@mock.patch("aes.main.encrypt_from_path")
def test_encrypt_from_path_value_error(encrypt_mock):
    encrypt_mock.side_effect = ValueError

    runner = CliRunner()
    result = runner.invoke(cli, ["encrypt", "filepath"])

    assert result.exit_code == 1
    assert "Error:" in result.output

    encrypt_mock.assert_called_once_with("filepath")


@mock.patch("aes.main.decrypt_from_path")
def test_decrypt_from_path_good(decrypt_m):
    runner = CliRunner()
    result = runner.invoke(cli, ["decrypt", "filepath"])

    assert result.exit_code == 0
    assert result.output == ""

    decrypt_m.assert_called_once_with("filepath")


@mock.patch("aes.main.decrypt_from_path")
def test_decrypt_from_path_decryption_error(decrypt_m):
    decrypt_m.side_effect = InvalidToken

    runner = CliRunner()
    result = runner.invoke(cli, ["decrypt", "filepath"])

    assert result.exit_code == 1
    assert "Invalid password" in result.output

    decrypt_m.assert_called_once_with("filepath")


@mock.patch("aes.main.decrypt_from_path")
def test_decrypt_from_path_value_error(decrypt_m):
    decrypt_m.side_effect = ValueError

    runner = CliRunner()
    result = runner.invoke(cli, ["decrypt", "filepath"])

    assert result.exit_code == 1
    assert "Error:" in result.output

    decrypt_m.assert_called_once_with("filepath")


@mock.patch("aes.main.cli")
def test_main(cli_m):
    main()
    cli_m.assert_called_once_with(prog_name="aes")
