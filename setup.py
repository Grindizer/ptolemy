#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "jsonschema<2.6",
    "PyYAML==3.11"
]

setup(
    name="ptolemy",
    version="1.0.0",
    description="Write terse AWS DMS table mappings.",
    long_description=readme + "\n\n" + history,
    author="James Routley",
    author_email="jroutley@gmail.com",
    url="https://github.com/cloudreach/ptolemy",
    packages=[
        "ptolemy"
    ],
    package_dir={
        "ptolemy": "ptolemy"
    },
    entry_points={
        "console_scripts": [
            "ptolemy=ptolemy.cli:main"
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords="ptolemy",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    test_suite="tests"
)
