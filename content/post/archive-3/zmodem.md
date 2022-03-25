---
title: Zmodem
author: "-"
date: 2019-04-15T07:00:08+00:00
url: /?p=14181
categories:
  - Uncategorized

tags:
  - reprint
---
## Zmodem
Zmodem: Zmodem采用了串流式 (streaming) 传输方式，传输速度较快，而且还具有自动改变区段大小和断点续传、快速错误侦测等功能。这是目前最流行的文件传输协议

SecureCRT默认上传下载目录

options->session options ->Terminal->Xmodem/Zmodem

Zmodem transfer canceled by remote side
  
在服务器上使用rz上传本地的文件到服务器时，出现一坨乱码，并报如下错误: 

"Zmodem transfer canceled by remote side "
  
网上查资料，根据大家建议的方法在rz上传文件的时候，加上-be参数即可解决问题。

rz -be file
  
参数解释: 

-b 以二进制方式传输 (binary) 。

-e 对控制字符转义 (escape) ，这可以保证文件传输正确。

参考网址: http://chenpeng.info/html/3473

https://blog.csdn.net/shanliangliuxing/article/details/7834937
  
https://blog.51cto.com/damaicha/1868613