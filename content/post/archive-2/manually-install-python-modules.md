---
title: manually install python modules
author: "-"
date: 2018-06-20T16:03:05+00:00
url: /?p=12342
categories:
  - Inbox
tags:
  - reprint
---
## manually install python modules

<https://stackoverflow.com/questions/32798137/importerror-no-module-named-appdirs>
  
download modules from pypi.python.org

wget <https://pypi.python.org/packages/48/69/d87c60746b393309ca30761f8e2b49473d43450b150cb08f3c6df5c11be5/appdirs-1.4.3.tar.gz>
  
gunzip appdirs-1.4.3.tar.gz
  
tar -xvf appdirs-1.4.3.tar
  
cd appdirs-1.4.3
  
sudo python setup.py install
