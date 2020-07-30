from pathlib import Path
from unittest import mock

import pytest

from aes import main


@pytest.mark.skip
@mock.patch("aes.main.main")
def test_main(main_mock):
    main(5, True)
    main_mock.assert_called_once_with(5, True)


@pytest.mark.skip
def test_get_version():
    version_path = Path(__file__).parent.parent.parent.joinpath("aes/VERSION")
    assert version_path.read_text().strip() == get_version()
