#!/usr/bin/env python
# coding: utf-8

# In[5]:

from setuptools import setup,find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Array simple product'

# Setting up
setup(
    name="multiptesttry",
    version=VERSION,
    author="Aimane",
    author_email="<aelmaimouni@leyton.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'product', 'tensors', 'arrays'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)



