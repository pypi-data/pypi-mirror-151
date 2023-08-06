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
    version = "0.0.3",
    description = "a package to load my own dataset",
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license = "MIT Licence",
    url="https://github.com/zemengchuan/thegreatdataset",
    project_urls = {
	"thegreatdataset":"https://github.com/zemengchuan/thegreatdataset",
    },
    author = "zemengchuan",
    author_email = "zemengchuan@gmail.com",
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ],

    packages =find_packages(),
    data_files = ["great_dataset.dataset"],
    include_package_data = True,
    install_requires = ['pandas'],
    platforms = "any",
)
