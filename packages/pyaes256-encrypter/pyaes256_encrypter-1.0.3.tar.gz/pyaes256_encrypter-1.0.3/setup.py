from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pyaes256_encrypter',
    version='1.0.3',
    url='https://github.com/MaiconRenildo/pyaes256_encrypter',
    license='MIT License',
    author='Maicon Renildo',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='maicon.renildo1@gmail.com',
    keywords='aes256',
    description=u'A package to simplify the use of AES-256 encryption with random initialization vector.',
)