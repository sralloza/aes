from unittest import mock

import pytest
from aes.general import decrypt_from_path, encrypt_from_path, temp_open


class TestEncryptFromPath:
    @pytest.fixture(autouse=True)
    def mocks(self):
        self.path_m = mock.patch("aes.general.Path").start()
        self.encr_folder_m = mock.patch("aes.general.encrypt_folder").start()
        self.ens_filepath_m = mock.patch("aes.general.ensure_filepath").start()
        self.encr_file_m = mock.patch("aes.general.encrypt_file").start()

        yield
        mock.patch.stopall()

    @pytest.mark.parametrize("password", [None, "pass"])
    @pytest.mark.parametrize("is_folder", [False, True])
    def test_encrypt_from_path(self, is_folder, password):
        self.path_m.return_value.is_dir.return_value = is_folder

        encrypt_from_path("input-path", password)

        self.path_m.assert_called_once_with("input-path")
        if is_folder:
            self.encr_folder_m.assert_called_once_with(
                self.path_m.return_value, password
            )
            self.ens_filepath_m.assert_not_called()
            self.encr_file_m.assert_not_called()
        else:
            self.encr_folder_m.assert_not_called()
            self.ens_filepath_m.assert_called_once_with(self.path_m.return_value)
            self.encr_file_m.assert_called_once_with(
                self.ens_filepath_m.return_value, password
            )


class TestDecryptFromPath:
    @pytest.fixture(autouse=True)
    def mocks(self):
        self.path_m = mock.patch("aes.general.Path").start()
        self.decr_folder_m = mock.patch("aes.general.decrypt_folder").start()
        self.ens_filepath_m = mock.patch("aes.general.ensure_filepath").start()
        self.decr_file_m = mock.patch("aes.general.decrypt_file").start()

        yield
        mock.patch.stopall()

    @pytest.mark.parametrize("password", [None, "pass"])
    @pytest.mark.parametrize("is_folder", [False, True])
    def test_decrypt_from_path(self, is_folder, password):
        self.path_m.return_value.is_dir.return_value = is_folder

        decrypt_from_path("input-path", password)

        self.path_m.assert_called_once_with("input-path")
        if is_folder:
            self.decr_folder_m.assert_called_once_with(
                self.path_m.return_value, password
            )
            self.ens_filepath_m.assert_not_called()
            self.decr_file_m.assert_not_called()
        else:
            self.decr_folder_m.assert_not_called()
            self.ens_filepath_m.assert_called_once_with(self.path_m.return_value)
            self.decr_file_m.assert_called_once_with(
                self.ens_filepath_m.return_value, password
            )


class TestTempOpen:
    def middle(self):
        self.efp_m.assert_not_called()
        self.dfp_m.assert_called_once_with("filepath", "password")

    @pytest.fixture(autouse=True)
    def mocks(self):
        self.efp_m = mock.patch("aes.general.encrypt_from_path").start()
        self.dfp_m = mock.patch("aes.general.decrypt_from_path").start()
        self.getchar_m = mock.patch("aes.general.click.getchar").start()
        self.getchar_m.side_effect = self.middle

        yield
        mock.patch.stopall()

    def test_temp_open(self):
        temp_open("filepath", "password")
        self.efp_m.assert_called_once_with("filepath", "password")
        self.dfp_m.assert_called_once_with("filepath", "password")
        self.getchar_m.assert_called_once()
