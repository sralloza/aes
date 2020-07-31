from aes import __version__
from aes._version import get_versions


def test_get_versions():
    real_version = get_versions()["version"]
    assert real_version == __version__
