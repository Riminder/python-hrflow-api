# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements


here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join("hrflow", "__version__.py"), "r") as f:
    exec(f.read(), about)

setup(
    # so far ignore paragraph embedding part for package
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],
    packages=find_packages(),
    install_requires=["requests", "python-magic"],
    python_requires=">=3.5",
    zip_safe=False,
)
