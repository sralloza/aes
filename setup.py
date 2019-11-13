import sys
from pathlib import Path

from setuptools import setup
from setuptools.command.test import test as TestCommand


def get_version():
    return Path(__file__).with_name("aes").joinpath("VERSION").read_text()


version = get_version()


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name="aes",
    url="https://git.sralloza.es/git/aes.git",
    description="AES 128-bit encryption for python",
    version=version,
    author="SrAlloza",
    entry_points={"console_scripts": ["aes=aes.main:main"],},
    include_package_data=True,
    author_email="admin@sralloza.es",
    packages=["aes", "aes.test"],
    install_requires=["cryptography"],
    package_data={"aes.test": ["test_data/ensure_filepath/*"]},
    tests_require=["pytest"],
    cmdclass={"test": PyTest},
    zip_safe=False,
)
