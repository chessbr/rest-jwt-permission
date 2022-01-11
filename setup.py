# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="django3-rest-jwt-permission",
    version="1.0.1",
    description="Django3 Rest Framework JWT Permissions",
    license="MIT",
    author="Rati Matchavariani",
    author_email="rati.matchavariani@hellotend.com",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tend/rest-jwt-permission",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Environment :: Web Environment",
        "Topic :: Internet :: WWW/HTTP",
        "Intended Audience :: Developers"
    ]
)
