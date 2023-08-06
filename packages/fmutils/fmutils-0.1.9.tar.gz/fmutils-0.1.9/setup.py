# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.1.9'
DESCRIPTION = "Package for easily accessing and managing large number of files and dirs (e.g. in ML datasets)."

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
INSTALL_REQUIRES = [
                    'numpy'
                    ]
# Setting up
setup(

        name="fmutils", 
        version=VERSION,
        author="Talha Ilyas",
        LICENSE = 'MIT License',
        author_email="mr.talhailyas@gmail.com",
        description=DESCRIPTION,
        long_description= long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES, 
        
        url = 'https://github.com/Mr-TalhaIlyas/FMUtils',
        
        keywords=['python', 'directory tree generator', 'files management', 
                'directory management','files listing', 'directories listing', 
                  'deleting files', 'randomly selecting file', 'transformer', 'IQA'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
)