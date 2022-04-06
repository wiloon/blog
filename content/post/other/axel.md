---
title: axel
author: "-"
date: 2012-12-02T12:28:38+00:00
url: /?p=4820

categories:
  - inbox
tags:
  - reprint
---
## axel
Axel 通过打开多个 HTTP/FTP 连接来将一个文件进行分段下载，从而达到加速下载的目的。对于下载大文件，该工具将特别有用。

```bash
  
#安装: 
  
sudo apt-get install axel
  
sudo pacman -S axel

axel -s 102400 https://download.jetbrains.8686c.com/idea/ideaIU-2017.1.2.tar.gz

```

-s: 限速: 如 -s 102400，即每秒下载的字节数，这里是 100 KB  
-n: 限制连接数: 如 -n 5，即打开 5 个连接  

下载目录会有一个.st文件, 会自动断点续传

http://linuxtoy.org/archives/axel.html