---
title: python basic
author: "-"
date: 2013-03-24T02:25:43+00:00
url: /?p=5343
categories:
  - inbox
tags:
  - reprint
---
## python basic

## 查看python的版本

python -V

### ubuntu

sudo apt install python3
sudo apt install -y python3-venv
mkdir python3-env
cd python3-env
python3 -m venv my_env
source my_env/bin/activate

><https://www.digitalocean.com/community/tutorials/ubuntu-18-04-python-3-zh>

### debian

Download latest release of Python

Fetch and extract source. Please refer to <http://www.python.org/download/releases> to ensure the latest source is used.

wget <http://www.python.org/ftp/python/3.x/Python-3.x.tar.bz2>
  
3- Extract and cd the extracted directory

tar -xjf Python-3.xtar.bz2 cd Python-3.x
  
4- Configure the build with a prefix (install dir) of /opt/python3, compile, and install.

./configure -prefix=/opt/python3
  
make
  
sudo make install
  
Python 3 will now be installed to /opt/python3.

$ /opt/python3/bin/python3 -V Python 3.x
  
5- Ensure your python 3 scripts and applications query the correct interpreter.

# !/opt/python3/bin/python3

That is all.
  
<http://www.unixmen.com/howto-install-python-3-x-in-ubuntu-debian-fedora-centos/>

### archlinux

    pacman -S python
  
### boolean variable

直接定义a=True/False就行，示例代码：

# 定义布尔值类型参数a,b，值分别为True,False

a=True

b=False

print a,b

print type(a),type(b)

## python 遍历目录

<http://www.cnblogs.com/vivilisa/archive/2009/03/01/1400968.html>

<http://laocao.blog.51cto.com/480714/525140>

[python]

# !/usr/bin/python
  
import os,sys
  
dir = '/home/wiloon/tmp'
  
list = os.listdir(dir)
  
print list

for line in list:

path = os.path.join(dir, line)

print path

[/python]
