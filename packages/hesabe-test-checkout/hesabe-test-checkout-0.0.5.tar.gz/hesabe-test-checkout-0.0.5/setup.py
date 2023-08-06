from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.0.5'
DESCRIPTION = 'checkout test package'
LONG_DESCRIPTION = 'checkout test package'
# Setting up
setup(
name="hesabe-test-checkout",
version=VERSION,
author="KL",
author_email="sounak.karmaalab@gmail.com",
description=DESCRIPTION,
long_description_content_type="text/markdown",
long_description=LONG_DESCRIPTION,
packages=find_packages(),
install_requires=['requests', 'pycryptodome'],
keywords=['python', 'django', 'hesabe'],
classifiers=[
"Development Status :: 1 - Planning",
"Intended Audience :: Developers",
"Programming Language :: Python :: 3",
"Operating System :: Unix",
"Operating System :: MacOS :: MacOS X",
"Operating System :: Microsoft :: Windows",
]
)