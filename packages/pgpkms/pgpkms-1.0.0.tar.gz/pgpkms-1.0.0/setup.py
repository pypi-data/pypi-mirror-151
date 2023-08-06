#!/usr/bin/env python

from setuptools import setup

params = {
  'name': 'pgpkms',
  'packages': [ 'pgpkms' ],
  'version': '1.0.0',
  'license': 'apache-2.0',
  'description': 'PGP signatures with AWS KMS keys',
  'author': 'Juit Developers',
  'author_email': 'developers@juit.com',
  'url': 'https://github.com/juitnow/pgpkms',
  'maintainer': 'Juit Developers <developers@juit.com>',
  'python_requires': '>=3.5',
  'keywords': [
    'AWS',
    'GnuPG',
    'KMS',
    'OpenPGP',
    'PGP',
    'RFC4880',
  ],
  'install_requires': [
    'botocore>=1.23.34',
    'pyasn1>=0.4.8',
    'pyasn1_modules>=0.2.1',
  ],
  'classifiers': [
    'Topic :: Security',
    'Topic :: Security :: Cryptography',
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
  ],
}

if __name__ == "__main__":
  setup(**params)
