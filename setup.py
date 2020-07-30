from pathlib import Path

from setuptools import find_packages, setup

from versioneer import get_cmdclass, get_version


def get_requirements():
    reqs = Path(__file__).with_name("requirements.txt")
    return [x.strip() for x in reqs.read_text().splitlines() if x.strip()]


setup(
    name="aes",
    url="https://github.com/sralloza/aes",
    description="AES 128-bit encryption for python",
    version=get_version(),
    author="Diego Alloza González",
    entry_points={"console_scripts": ["aes=aes.main:main"],},
    include_package_data=True,
    author_email="aes-support@sralloza.es",
    packages=find_packages(),
    install_requires=get_requirements(),
    tests_require=["pytest", "coverage"],
    cmdclass=get_cmdclass(),
    zip_safe=False,
)
