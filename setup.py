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
    # package name
    name='hrflow',
    # code version
    version="1.5.3",
    # so far ignore paragraph embedding part for package
    packages=find_packages(),
    author="Riminder",
    author_email="contact@rimider.net",
    description="Hrflow API",
    license='MIT',
    install_requires=reqs,
    include_package_data=True,
    package_data={'hrflow': ['drawers/prod_ner_drawer_icons/*.png']},
    long_description=open('README.md').read(),
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.6",
    ]
)
