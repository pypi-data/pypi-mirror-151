from setuptools import setup, find_packages
import codecs
import os
from setup_utils import get_list_of_names

# here = os.path.abspath(os.path.dirname(__file__))
#
with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.1.0'
DESCRIPTION = 'Python SDK for frontend components usage'
LONG_DESCRIPTION = 'A package that allows to use front-end components to simplify ' \
                   'building of web pages for ekp plugins'

# Setting up
setup(
    name="ekp-sdk",
    version=VERSION,
    url="https://github.com/earnkeeper/python-ekp-sdk",
    author="Earn Keeper (Gavin Shaw)",
    author_email="gavin@earnkeeper.io",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=get_list_of_names('top_level_imports'),
    packages=find_packages(),
    install_requires=get_list_of_names('requirements.txt'),
    keywords=['python', 'earnkeeper', 'sdk', 'ekp'],
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        # "Operating System :: Unix",
        # "Operating System :: MacOS :: MacOS X",
        # "Operating System :: Microsoft :: Windows",
    ]
)
