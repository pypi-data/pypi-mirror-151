#!/usr/bin/env python3

from pathlib import Path
from setuptools import setup

REPO_ROOT = Path(__file__).resolve().parent


with open(REPO_ROOT / "README.md") as f:
    readme = f.read()

# https://setuptools.readthedocs.io/en/latest/setuptools.html
setup(
    name="apylaas",
    description="Any Python Library As A Service",
    long_description=readme,
    long_description_content_type="text/markdown",
    version="0.0.1",
    # author=about['__author__'],
    # author_email=about['__author_email__'],
    packages=["apylaas"],
    python_requires=">=3.7.*",
    install_requires=[],
    license="MIT",
    entry_points={
        "console_scripts": ["apylaas = apylaas:main"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
    ],
)
