from setuptools import setup


from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="fhir_biobank",
    version="0.1.3",
    description="Python library working with FHIR standard in scope of biobanks MIABIS requirements",
    long_description=long_description,
    long_description_content_type= "text/markdown",
    url="https://fhir-biobank.readthedocs.io/",
    author="Simon Konar",
    author_email="simon.konar@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ],
    packages=["fhir_biobank"],
    include_package_data=True,
    install_requires=["fhirclient", "pytest"]
)