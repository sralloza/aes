from setuptools import setup

setup(
    name='AES',
    version='b1.1',
    packages=['aes'],
    scripts=['aes/scripts/aes.py'],
    install_requires=['cryptography']
)
