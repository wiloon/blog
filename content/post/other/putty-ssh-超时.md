---
title: putty ssh 超时
author: "-"
date: 2014-03-13T06:14:44+00:00
url: /?p=6397
categories:
  - Inbox
tags:
  - Linux

---
## putty ssh 超时
http://blog.fens.me/putty-timeout/
  
    用Putty进行SSH连接的时候，如果几分钟没动，就会出现断线的情况，然后Putty客户端就死了。
  
  
    为了解决这个问题，我们需要让客户端与Server端，一直保持发包状态，就可以避免Putty断线的情况。
  
  
    操作如下: 
  
  
    putty –>Connection –> Seconds Between keepalives –>60
  
