#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from setuptools import setup

# Package meta-data.
NAME = 'todoist-template'
DESCRIPTION = 'Easily add tasks to Todoist with custom templates.'
URL = 'https://github.com/jamesbrond/todoist-template'
EMAIL = 'jamesbrond@gmail.com'
AUTHOR = 'Diego Brondo'
REQUIRES_PYTHON = '>=3.8.0'
VERSION = None

# What packages are optional?
EXTRAS = {}


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join('docs', 'README.md'), 'r', encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
with io.open(os.path.join(NAME, 'lib', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

# I only have to maintain requirements.txt
# and no duplication of same in setup.py
with io.open('requirements.txt', 'r', encoding='utf8') as f:
    requirements = f.read().splitlines()


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=['todoist-template', 'todoist-template.lib', 'todoist-template.lib.loader'],
    install_requires=requirements,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Communications :: Email',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Bug Tracking'
    ]
)

# ~@:-]
