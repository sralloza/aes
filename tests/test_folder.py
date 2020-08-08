from unittest import mock
from pathlib import Path

import pytest

from aes.folder import decrypt_folder, encrypt_folder

WALK_FILES = (
    (".", ["folder"], ["1.txt", "2.txt", "3.txt"]),
    ("./folder", [], ["newa.txt", "newb.txt"]),
)

REAL_FILES = ["./1.txt", "./2.txt", "./3.txt", "./folder/newa.txt", "./folder/newb.txt"]


class TestEncryptFolder:
    @pytest.fixture(autouse=True)
    def mocks(self):
        self.walk_m = mock.patch("aes.folder.walk").start()
        self.walk_m.return_value = WALK_FILES
        self.encr_file_m = mock.patch("aes.folder.encrypt_file").start()

        yield

        mock.patch.stopall()

    def test_encrypt_folder(self):
        encrypt_folder("filepath")
        self.walk_m.assert_called_once_with(Path("filepath"))
        for file in REAL_FILES:
            file = Path(file)
            self.encr_file_m.assert_any_call(file, None)



class TestDecryptFolder:
    @pytest.fixture(autouse=True)
    def mocks(self):
        self.walk_m = mock.patch("aes.folder.walk").start()
        self.walk_m.return_value = WALK_FILES
        self.decr_file_m = mock.patch("aes.folder.decrypt_file").start()

        yield

        mock.patch.stopall()

    def test_decrypt_folder(self):
        decrypt_folder("filepath")
        self.walk_m.assert_called_once_with(Path("filepath"))
        for file in REAL_FILES:
            file = Path(file)
            self.decr_file_m.assert_any_call(file, None)
