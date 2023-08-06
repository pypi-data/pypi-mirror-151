import os
from setuptools import setup, find_packages


path = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(path, 'README.md')) as f:
        long_description = f.read()
except Exception as e:
    long_description = "load my own dataset"

setup(
    name = "thisismygreatdataset",
    version = "0.0.1",
    keywords = ("pip", "dataset"),
    description = "a package to load my own dataset",
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license = "MIT Licence",

    url = "https://github.com/zemengchuan/thegreatdataset",
    author = "zemengchuan",
    author_email = "zemengchuan@gmail.com",

    packages =find_packages(),
    include_package_data = True,
    install_requires = ['pandas'],
    platforms = "any",
)
