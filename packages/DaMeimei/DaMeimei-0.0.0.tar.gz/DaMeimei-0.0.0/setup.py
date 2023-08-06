#!/usr/bin/env python
# coding: utf-8
import setuptools


setuptools.setup(
    name='DaMeimei',
    version='0.0.0',
    author='Tong',
    author_email='3231690635@qq.com',
    description='tong\'s physic library',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
