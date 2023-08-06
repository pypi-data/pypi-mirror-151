#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "TwinClient",
    version = "0.1.2",
    url = 'https://github.com/sxhxliang',
    long_description_content_type="text/markdown",
    long_description = open('README.md').read(),
    packages = find_packages(),
    author='Shihua Liang',
    author_email='sxhx.liang@gmail.com',
    description='twin client sdk',
    install_requires=['pydantic'],
    python_requires='>=3.6',
)