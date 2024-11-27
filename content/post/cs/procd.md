---
title: procd
author: "-"
date: 2019-01-28T14:55:10+00:00
url: /?p=13512
categories:
  - Inbox
tags:
  - reprint
---
## procd
https://openwrt.org/docs/guide-developer/procd-init-scripts
  
https://blog.csdn.net/liangdsing/article/details/53906445

```bash
#!/bin/sh /etc/rc.common
# Copyright (C) 2008 OpenWrt.org

#执行的顺序,按照字符串顺序排序并不是数字排序
START=98

#使用procd启动
USE_PROCD=1

#start_service 函数必须要重新定义
start_service() {
    #创建一个实例, 在procd看来一个应用程序可以多个实例
    procd_open_instance
    #定义respawn参数,告知procd当binloader程序退出后尝试进行重启
    procd_set_param respawn
    # binloader执行的命令是"/usr/bin/binloader", 若后面有参数可以直接在后面加上
    procd_set_param command "$BINLOADER_BIN"

    #关闭实例
    procd_close_instance

}

#stop_service重新定义,退出服务器后需要做的操作
stop_service() {
    rm -f /var/run/binloader.pid
}

restart() {
    stop
    start
}

```

  1. start_service() 为注册服务到procd中,如果自己的应用程序没有配置文件,只要实现start_service()就好, procd_set_param设置设置好多参数,command为自己的应用路径, respawn可以检测自己的应用,如果挂掉可以重启,也可以设置重启间隔,其它参数可以自己查阅。 
  2. stop_service() 这个时procd kill自己的应用程序后调用的,若果你的应用程序关掉后,需要一些清理工作,需要实现这个。

  3. service_triggers() 如果自己的应用需要关联一个配置文件test, (需要放在/etc/config/目录下) ,可以跟踪文件的修改情况,如果这个文件有改变,就调用reload_service().在service_triggers也可以添加跟踪网络的修改,也可以同时跟踪多个配置文件。

  4. reload_service() 配置文件改变后,需要调用这个函数,可以根据自己需要实现功能。

注: start和reload区别是,start一般是指应用程序启动, reload一般是指只是重新加载与配置文件改变相关的部分,不把整个应用程序重新启动。这种方式应该是推荐的,如果你再reload里重新启动应用也是可以的。

http://www.voidcn.com/article/p-ymidazab-bqa.html