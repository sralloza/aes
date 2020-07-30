from unittest import mock
from aes import main, get_version
from pathlib import Path

@mock.patch("aes.cli.main")
def test_main(main_mock):
    main(5, True)
    main_mock.assert_called_once_with(5, True)


def test_get_version():
    version_path = Path(__file__).parent.parent.parent.joinpath("aes/VERSION")
    assert version_path.read_text().strip() == get_version()
