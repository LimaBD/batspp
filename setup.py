#!/usr/bin/env python3
#
# Setup
#


"""Setup"""


# Standard packages
import setuptools
import os


package_root = os.path.abspath(os.path.dirname(__file__))

# Version
version = {}
with open(os.path.join(package_root, "batspp/version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]

# Readme
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Requirements
with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="batspp",
    version=version,
    author="Bruno Daniel Lima",
    author_email="bdl1998@hotmail.com",
    description="Shell style tests using bats-core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LimaBD/batspp",
    project_urls={
        "Bug Tracker": "https://github.com/LimaBD/batspp/issues",
    },
    license='GNU Lesser General Public License v3 (LGPLv3)',
    license_files=("LICENSE.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    scripts=['batspp/batspp'],
    package_dir={"": "batspp"},
    python_requires=">=3.8",
    install_requires=required,
)
