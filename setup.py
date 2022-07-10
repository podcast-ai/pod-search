#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

# with open("requirements.txt") as requirements_file:
#     requirements = requirements_file.readlines()

# with open("requirements_dev.txt") as dev_requirements_file:
#     dev_requirements = dev_requirements_file.readlines()

setup(
    author="Podcast AI Hackathon Team",
    author_email="mail@clstaudt.me",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Podcast content search engine.",
    # install_requires=requirements + dev_requirements,
    # license="GNU General Public License v3",
    long_description=readme + "\n\n",
    include_package_data=True,
    keywords="podcast",
    name="podcatch",
    packages=find_packages(include=["podcatch", "podcatch.*"]),
    test_suite="tests",
    version="0.1",
    zip_safe=False,
)
