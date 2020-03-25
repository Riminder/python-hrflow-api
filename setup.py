# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

FILE_PATH = os.path.dirname(os.path.realpath(__file__))

install_reqs = parse_requirements(os.path.join(FILE_PATH, 'requirements.txt'), session="hack")
reqs = [ir.req.__str__() for ir in install_reqs]

setup(
    # so far ignore paragraph embedding part for package

    name='hrflow',
    version='1.6.2',
    description='python hrflow api package',
    #long_description=open('README.md', 'rt').read(),
    #long_description_content_type="text/markdown",
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
