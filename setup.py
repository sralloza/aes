from setuptools import setup

setup(
    name='aes',
    version='b1.2',
    packages=['aes'],
    scripts=['aes/scripts/aes.py'],
    install_requires=['cryptography']
)
