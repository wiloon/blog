---
title: linux enca 编码并转换
author: "-"
date: 2017-10-31T12:53:47+00:00
url: /?p=11354
categories:
  - Inbox
tags:
  - reprint
---
## linux enca 编码并转换
enca -list languages
  
enca -L zh_CN file 检查文件的编码
  
enca -L zh_CN -x UTF-8 file 将文件编码转换为"UTF-8″编码
  
enca -L zh_CN -x UTF-8 < file1 > file2 如果不想覆盖原文件可以这样
  
enca -L none file.txt

http://os.51cto.com/art/201007/214344.htm
  
http://www.shenyanchao.cn/blog/2014/11/13/encode-convert-in-linux/
  
http://54im.com/tag/enca