#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from pass_audit import __version__

__url__ = 'https://github.com/roddhjav/pass-audit'

setup(
    name="pass-audit",
    version=__version__,
    author="Alexandre Pujol",
    author_email="alexandre@pujol.io",
    url=__url__,
    download_url="%s/releases/download/v%s/pass-import-%s.tar.gz"
                 % (__url__, __version__, __version__),
    description="A pass extension for auditing your password repository.",
    license='GPL3',

    py_modules=['pass_audit'],

    install_requires=[
        'requests',
        'zxcvbn'
        ],
    tests_require=[
        'green'
        ],
    test_suite='tests',
    python_requires='>=3.5',

    keywords=[
        'password-store', 'password', 'pass', 'pass-extension',
        'audit', 'password-audit', 'haveibeenpwned',
        ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Security :: Cryptography',
        ],
)
