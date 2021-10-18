---
title: python basic
author: "-"
type: post
date: 2013-03-24T02:25:43+00:00
url: /?p=5343

---
# python basic
# python
### ubuntu
sudo apt install python3
sudo apt install -y python3-venv
mkdir python3-env
cd python3-env
python3 -m venv my_env
source my_env/bin/activate

>https://www.digitalocean.com/community/tutorials/ubuntu-18-04-python-3-zh
### debian
Download latest release of Python

Fetch and extract source. Please refer to http://www.python.org/download/releases to ensure the latest source is used.

wget http://www.python.org/ftp/python/3.x/Python-3.x.tar.bz2
  
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
  
http://www.unixmen.com/howto-install-python-3-x-in-ubuntu-debian-fedora-centos/

### archlinux 
    pacman -S python
  
