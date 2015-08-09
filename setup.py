# -*- coding: utf-8 -*-
"""
Cytisas is a suit for python project. It have will realize serveral libraries in
Python by myself.
"""

from setuptools import setup, find_packages

URL = "https://github.com/OctavianLee/Cytisas"
VERSION = "0.0.0"

setup(
    name="cytisas",
    version=VERSION,
    license='MIT',
    author="Octavian Lee",
    author_email="octavianlee1@gmail.com",
    url=URL,
    description="A suite for python project.",
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
)
