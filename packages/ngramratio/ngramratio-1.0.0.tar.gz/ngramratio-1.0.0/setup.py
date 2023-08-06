#!/usr/bin/env python


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ngramratio",
    version="1.0.0",
    author="Giacomo Baldo",
    author_email="baldogiacomophd@gmail.com",
    description="N-grams based similarity score",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gi-ba-bu/python-n-gram-ratio",
    project_urls={
        "Bug Tracker": "https://github.com/gi-ba-bu/python-n-gram-ratio/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
