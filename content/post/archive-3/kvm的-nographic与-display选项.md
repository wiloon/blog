---
title: KVM 的-nographic与-display选项
author: "-"
date: 2019-03-31T02:18:40+00:00
url: /?p=14053
categories:
  - Uncategorized

tags:
  - reprint
---
## KVM 的-nographic与-display选项

KVM的-nographic与-display选项
http://openwares.net/2014/03/10/kvm_nographic_display/

KVM的-nographic与-display选项&
http://openwares.net/2014/03/10/kvm_nographic_display/embed/#?secret=cEd7rLTTHt

KVM客户机正常运行时是不需要在主机上显示图形界面的,以前都是使用-nographic和-daemoniz选项来使客户机后台运行。
但是从qemu-kvm 1.4开始,这招不灵了，会有这样的错误提示:
-nographic can not be used with -daemonize
  
这提示过于简单的,新版本的kvm不再允许-nographic和-daemonize一起使用了,应该使用-display none参数来代替-nographic,这样:

kvm ...
  
-display none
  
-daemonize
  
-display参数用于替代老风格的显示类型选项,如-sdl,-curses,-vnc，其语法如下:

-display [sdl | curses | vnc=<display>]
  
其中,vnc=<display>中的display与显示环境变量$DISPLAY的含义一致,格式为hostname: displaynumber.screennumber(X服务器主机名/地址:显示号.屏幕号)。一般设置为vnc=:0即可,如果有多台虚拟机在同一台主机上需要同时使用VNC,则每台客户机的显示号顺延就可,比如:1,:2,:3等,而通过vnc客户端连接客户机的端口号则分别为5900,5901,5902,5903。5900是默认的vnc端口,对应显示设备:0。

使用-display none选项时,客户机仍然会看到模拟的显卡，但是其显示不会输出给用户。
  
-display none与-nographic的区别是,-display none仅仅影响显示输出,而-nographic同时还会影响串行口和并行口的输出。

-nographic和-daemonize组合一直以来存在一个小问题,kvm客户机启动后,主机虚拟终端后续的命令回显会被关闭,但命令的输出会显示，只能退出重新登录终端才会恢复正常，这是个很明显的bug,却很久都没有修复。改用-display none参数后就没有此问题了。

kvm更详细的用法,请自行 man qemu