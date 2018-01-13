# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="rest-jwt-permission",
    version="0.2.0",
    description="Django Rest Framework JWT Permissions",
    license="MIT",
    author="Christian Hess",
    author_email="christianhess.rlz@gmail.com",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    url="https://github.com/chessbr/rest-jwt-permission",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 2.7",
        "Environment :: Web Environment",
        "Topic :: Internet :: WWW/HTTP",
        "Intended Audience :: Developers"
    ]
)
