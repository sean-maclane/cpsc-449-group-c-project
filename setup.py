'''
This file was adapted from the flask documentation for our project
'''

import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="project1",
    version="1.0.0",
    license="MIT",
    maintainer="CPSC 440 Group C",
    description="A simple reddit clone backend",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", "pytest", "coverage", "locustio"],
)
