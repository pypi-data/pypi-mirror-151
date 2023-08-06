#!/usr/bin/env python
from setuptools import setup


def get_version():
    version_file = "nc_py_install/_version.py"
    with open(version_file) as f:
        exec(compile(f.read(), version_file, "exec"))
    return locals()["__version__"]


setup(version=get_version())
