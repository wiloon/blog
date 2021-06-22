---
title: centos vncserver
author: "-"
type: post
date: 2012-03-13T15:13:27+00:00
url: /?p=2556
categories:
  - Linux

---
CENTOS6的VNC SERVER
  
CENTOS6中的VNC SERVER已更換成tightvnc

因此要安裝tightvnc
  
[root@root ]# yum -y install tigervnc-server
  
[root@root ]# vncserver

[cent@root ]$ vncpasswd
  
# set VNC password

[cent@root ]$ Password:
  
# input password

[cent@root ]$ Verify:
  
# confirm password

啟動vncserver
  
[cent@root ]$ vncserver

Windows 端連線vncserver
  
IP:port
  
輸入密碼

tigervnc安裝完成便直接進入Xwindow 的畫面，比以前少一道修改xstartup步驟。