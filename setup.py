from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="toolkits",
    version="0.0.4",
    author="XH",
    author_email="605828203.com",
    description="A Python library for application.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/xuhuanyunxiao/toolkits.git",
    packages=['toolkits'],
    include_package_data=True, # 自动打包文件夹内所有数据
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Multimedia :: Video',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=True, # 设定项目包为安全，不用每次都检测其安全性
)