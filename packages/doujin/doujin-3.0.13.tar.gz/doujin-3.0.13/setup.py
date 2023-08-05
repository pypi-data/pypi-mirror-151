from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='doujin',
    version='3.0.13',
    url='https://github.com/sinkaroid/janda',
    author='janda',
    description='A mirror package for janda. Please install that instead.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[],
    install_requires=['janda>=3.0.12'],
)
