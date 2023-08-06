#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md', 'r') as f:
    readme = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='acido',
    packages=['acido'],
    version='0.0.8',
    description='Azure Container Instance Distributed Operations',
    long_description=readme,
    author='Xavier Álvarez',
    author_email='xalvarez@merabytes.com',
    url='https://github.com/merabytes/acido',
    license='MIT',
    install_requires=[
        'azure-cli>=2.18.0,<2.18.1',
        'azure-core>=1.10.0,<1.10.1',
        'azure.identity==1.3',
        'azure.keyvault.secrets',
        'azure.storage.blob',
        'websockets',
        'huepy',
        'msrestazure'
    ],
    keywords=[
        'Security',
        'Cloud Computing',
        'Red Team',
        'Pentesting'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)