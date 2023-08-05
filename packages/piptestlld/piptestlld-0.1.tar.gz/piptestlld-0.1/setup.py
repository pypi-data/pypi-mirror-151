#!/usr/bin/python
# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name="piptestlld",
    version="0.1",
    license="MIT Licence",


    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)


#关键参数说明:

# name的名称就是包的名称,别人可以使用pip install name安装的.
#
# version是版本号,这个很容易理解,后面更新的版本号要比这个高才行.
#
# packages是导入目录下的所有__init__.py包
#
# install_requires是引入的第三方的包,如果有版本号,也需要写上