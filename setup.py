# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements


setup(
    # so far ignore paragraph embedding part for package

    name='hrflow',
    version='1.6.5',
    description='python hrflow api package',
    url='https://github.com/hrflow/python-hrflow-api',
    author='riminder',
    author_email='contact@rimider.net',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-magic'
    ],
    python_requires='>=3.5',
    zip_safe=False
)
