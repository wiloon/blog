---
title: raspberry pi wn725n driver
author: wiloon
type: post
date: 2013-11-30T09:49:41+00:00
url: /?p=5994
categories:
  - Uncategorized

---
<http://www.raspberrypi.org/phpBB3/viewtopic.php?t=55779>

[http://lukin.cn/p/Raspberry\_Pi\_TP-LINK\_WN725N\_V2.html][1]

wget https://dl.dropboxusercontent.com/u/80256631/8188eu-20130209.tar.gz

for 3.6.11+ #538 and #541 use 8188eu-20130830.tar.gz
  
for 3.6.11+ #524, #528 or #532 use 8188eu-20130815.tar.gz
  
for 3.6.11+ #371 up to #520 use 8188eu-20130209.tar.gz

&nbsp;

    sudo install -p -m 644 8188eu.ko /lib/modules/`uname -r`/kernel/drivers/net/wireless
    sudo depmod -a
    sudo modprobe 8188eu

 [1]: http://lukin.cn/p/Raspberry_Pi_TP-LINK_WN725N_V2.html