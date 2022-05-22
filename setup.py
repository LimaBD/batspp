#
# TODO: add description
#


import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="batspp",
    version="1.1.0",
    author="Tom O\'Hara, Bruno Daniel Lima",
    author_email="tomasohara@gmail.com, bdl1998@hotmail.com",
    description="This process and run shell style tests using bats-core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LimaBD/batspp",
    project_urls={
        "Bug Tracker": "https://github.com/LimaBD/batspp/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    scripts=['batspp/batspp'],
    package_dir={"": "batspp"},
    packages=setuptools.find_packages(where="batspp"),
    python_requires=">=3.6",
)
