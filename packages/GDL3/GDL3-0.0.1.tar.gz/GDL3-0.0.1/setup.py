from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Game Development Package'
LONG_DESCRIPTION = 'This Package is a wrapper around pygame and uses pygame to make games quickly and easily!'

# Setting up
setup(
    name="GDL3",
    version=VERSION,
    author="ProgrammingBro (Akhil Ganta)",
    author_email="<srinivasganta123@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
