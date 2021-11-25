# -*- coding: utf-8 -*-
'''
    :file: setup.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/09/20 11:11:54
'''

from os import name, path
from setuptools import setup, find_packages

basedir = path.abspath(path.dirname(__file__))

with open(path.join(basedir, "README.md"), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="school-sdk",
    author="farmer.chillax",
    version="1.2.0",
    license='MIT',
    author_email="farmer-chong@qq.com",
    description="zf School SDK for Python",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Farmer-chong/new-school-sdk',
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    platforms='any',
    zip_safe=False,

    install_requires=[
        'requests',
        'pyquery',
        'bs4',
        'Pillow',
        'fake-headers'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)


# python setup.py bdist_wheel sdist
# twine upload dist/*