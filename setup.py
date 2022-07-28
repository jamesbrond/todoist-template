#!/usr/bin/env python

from setuptools import setup, find_packages

long_description = open('docs/README.md').read()

# I only have to maintain requirements.txt
# and no duplication of same in setup.py
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='todoist-template',
    version='1.0',
    description='Easily add tasks to Todoist with customizable templates',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    author='Diego Brondo',
    author_email='jamesbrond@gmail.com',
    url='https://github.com/jamesbrond/todoist-template',
    packages=find_packages(),
    install_requires=requirements,
)
