---
title: putty
author: "-"
date: 2014-03-13T06:14:44+00:00
url: /?p=6397
categories:
  - Inbox
tags:
  - Linux

---
## putty ssh 超时

[http://blog.fens.me/putty-timeout/](http://blog.fens.me/putty-timeout/)
  
    用Putty进行SSH连接的时候，如果几分钟没动，就会出现断线的情况，然后Putty客户端就死了。
  
  
    为了解决这个问题，我们需要让客户端与Server端，一直保持发包状态，就可以避免Putty断线的情况。
  
  
    操作如下: 
  
  
    putty –>Connection –> Seconds Between keepalives –>60

## 远程桌面 看不到 鼠标指针

[https://support.huawei.com/enterprise/zh/knowledge/EKB1000027195](https://support.huawei.com/enterprise/zh/knowledge/EKB1000027195)

windows版本:  windows server 2008 R2 Standard

1. 在控制面板中搜索"鼠标"，选择"更改鼠标指针的外观
2. 在"指针"标签页中，在"自定义"栏目里，找到"文本选择"项；
3. 选择"文本选择"，然后"浏览"定义鼠标图形，在弹出的对话框中选择"beam_r.cur"，确认即可。

根因

鼠标在putty (或者某些黑色编辑器) 中光标不能自动反白，可通过更改光标的样式来解决看不到光标的问题。

### win10

控制面板中搜索"鼠标 "

点击 "更改指针大小 和颜色"

选择 黑色
