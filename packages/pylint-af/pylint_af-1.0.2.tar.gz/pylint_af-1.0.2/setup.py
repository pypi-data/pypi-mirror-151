"""Module for packaging and distribution Python packages."""


import setuptools

with open("README.md", mode="r", encoding="utf8") as fh:
    long_description = fh.read()

requirements = ["pylint==2.13.9"]

setuptools.setup(
    name="pylint_af",
    version="1.0.2",
    author="Albert Farkhutdinov",
    author_email="albertfarhutdinov@gmail.com",
    description=(
        "The package that allows you to check the Python code "
        "for compliance with PEP8."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlbertFarkhutdinov/pylint_af",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
