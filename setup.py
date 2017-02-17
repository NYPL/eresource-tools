from sys import exit, version

from setuptools import setup, find_packages

if version < '3.1.0':
    print("python 3.1 or higher is required")
    exit(1)

description = \
"""
This package can be used to work with eresource preservation.
"""

# for older pythons ...
requirements = []
try:
    import bagit
except:
    requirements.append("xlrd")


setup(
    name = 'eresource_tools',
    version = 0.1,
    description = description,
    url = 'https://github.com/nypl/eresource-tools/',
    author = 'Nick Krabbenhoeft',
    author_email = 'nickkrabennhoeft@nypl.org',
    packages = find_packages(),
    scripts = ['extract_issn.py'],
    platforms = ['POSIX'],
    install_requires = ['xlrd'],
    classifiers = [
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
