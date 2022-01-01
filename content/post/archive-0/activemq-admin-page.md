---
title: size
author: "-"
date: 2012-07-12T04:17:32+00:00
url: size
categories:
  - linux

---
## size
size 程序列出参数列表中各目标文件或存档库文件的段大小 — 以及总大小。默认情况下，对每个目标文件或存档库中的每个模块都会产生一行输出。

    wiloonwy@penguin:~/tmp$ size foo 
      text    data     bss     dec     hex filename
      1458     584       8    2050     802 foo

前三部分的内容是文本段、数据段和 bss 段及其相应的大小。然后是十进制格式和十六进制格式的总大小。最后是文件名。