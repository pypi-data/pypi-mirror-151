#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    reshapedata LLC
"""
import platform
from setuptools import setup
from setuptools import find_packages

setup(
    name = 'rdwebapi',
    version = '1.0.1',
    install_requires=[
        'requests',
    ],
    packages=find_packages(),
    license = 'Apache License',
    author = 'hulilei',
    author_email = 'hulilei@takewiki.com.cn',
    url = 'http://www.reshapedata.com',
    description = 'R webApi test in py language ',
    keywords = ['reshapedata', 'rdwebapi'],
    python_requires='>=3.6',
)
