---
title: 网络唤醒 Wake On LAN
author: "-"
type: post
date: 2019-02-02T06:47:47+00:00
url: /?p=13531

---
android client

TX ToolBox

Name: 填写一个别名就可以,例如: foo
Mac Address: 填写电脑网卡MAC地址（注意是主板上有线网卡) ,这个要填写正确,如何获得? 进入命令行运行: ipconfig /all,然后查看对应的物理地址即可,共6组2字节十六进制字符；

Broadcast IP/Hostname/FQDN
Broadcast IP/Hostname 是电脑所在的局域网的广播地址: 如果你的电脑分配到192.168.1.100则填写192.168.1.255,将唤醒包广播到1网段下面所有电脑,Hostname:则是你电脑的主机名.
FQDN:是广域网唤醒,例如你的手机在公网（4g上网) ,不在局域网,则需要填写路由器的DDNS域名,如: http://homepc.router.net
Port 端口默认是9,这里默认就可以



windows

BIOS打开唤醒设置
  
在BIOS电源相关选项寻找Resume By LAN,Enable Wake ON LAN 类似选项开启
  
网卡设置
  
找到对应的网卡,打开可唤醒选项

勾选
  
允许计算机关闭此设备发节约电源
  
允许此设备唤醒计算机

