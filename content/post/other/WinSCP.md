---
title: WinSCP 的四种协议：SFTP(SSH)、FTP、SCP、WebDAV
author: "-"
date: 2014-12-23T10:20:54+00:00
url: WinSCP
categories:
  - Linux
tags:
  - reprint


---
## WinSCP的四种协议：SFTP(SSH)、FTP、SCP、WebDAV

1、FTP

FTP（File Transfer Protocol，文件传输协议），通过端口进行文件传输：
端口21，控制链路，用于发送指令给服务器并等待服务器响应；
端口20，数据链路，用来建立数据传输通道。
使用FTP协议可能会存在一些安全隐患，例如FTP服务器软件的漏洞、明文口令、通过FTP服务器进行端口扫描、数据劫持等。
参考：[https://baike.baidu.com/item/FTP协议/7651119?fr=aladdin](https://baike.baidu.com/item/FTP协议/7651119?fr=aladdin)

2.SFTP(SSH)

SSH (SSH File Transfer Protocol) 又称 SFTP(Secret File Transfer Protocol)，安全文件传送协议，为传输文件提供一种安全的加密方法。
SFTP是SSH内含的协议，只要SSHD服务器启动了就可用，不需要FTP服务器启动才能用。
对网络安全性要求高时，建议使用SFTP。由于SFTP采用加密传输认证信息和数据，所以SFTP十分安全，但是传输效率就比FTP要低的多。
参考：[https://baike.baidu.com/item/SSH文件传输协议?fromtitle=sftp&fromid=1184182](https://baike.baidu.com/item/SSH文件传输协议?fromtitle=sftp&fromid=1184182)

3、SCP

SCP（secure copy），用来进行远程文件拷贝，使用和SSH相同的认证方式，提供相同的安全保障。
参考：[https://www.cnblogs.com/mxh1099/p/5554823.html](https://www.cnblogs.com/mxh1099/p/5554823.html)

4、WebDAV

WebDAV一种基于HTTP1.1的扩展协议，
在GET、POST、HEAD等几个HTTP标准方法以外添加了一些新的方法，
使应用程序对Web Server直接读写，并支持写文件锁定及解锁，还可以支持文件的版本控制。
参考：[https://baike.baidu.com/item/WebDAV](https://baike.baidu.com/item/WebDAV)

>[https://www.cnblogs.com/bors/p/WinSCP.html](https://www.cnblogs.com/bors/p/WinSCP.html)
