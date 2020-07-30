import sys
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def get_version():
    return Path(__file__).with_name("aes").joinpath("VERSION").read_text().strip()


def get_requirements():
    reqs = Path(__file__).with_name("requirements.txt")
    return [x.strip() for x in reqs.read_text().split("\n") if x.strip()]


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
    url="https://github.com/sralloza/aes",
    description="AES 128-bit encryption for python",
    version=version,
    author="Diego Alloza González",
    entry_points={"console_scripts": ["aes=aes.main:main"],},
    include_package_data=True,
    author_email="aes-support@sralloza.es",
    packages=find_packages(),
    install_requires=get_requirements(),
    tests_require=["pytest", "coverage"],
    zip_safe=False,
)
