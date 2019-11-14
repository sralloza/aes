from unittest import mock
from aes import main, get_version


@mock.patch("aes.cli.main")
def test_main(main_mock):
    main(5, True)
    main_mock.assert_called_once_with(5, True)


def test_get_version():
    current_dir = __file__[: __file__.rindex("\\")]
    with open(current_dir + "//../../aes/VERSION", "rt") as file:
        assert get_version() == file.read().strip()
