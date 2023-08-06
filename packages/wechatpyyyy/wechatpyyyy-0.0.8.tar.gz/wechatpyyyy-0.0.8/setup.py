#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "wechatpyyyy",      #这里是pip项目发布的名称
    version = "0.0.8",  #版本号，数值大的会优先被pip
    keywords = ["pip", "wechatpyyyy"],			# 关键字
    description = "修改了一下request verify=false",	# 描述
    long_description = "xiaozhouzhou",
    license = "MIT Licence",		# 许可证

    url = "",     #项目相关文件地址，一般是github项目地址即可
    author = "xiaozhouzhou",			# 作者
    author_email = "zhoudabaoonline@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["optionaldict", "xmltodict", "python-dateutil", "requests", "six"]          #这个项目依赖的第三方库
)