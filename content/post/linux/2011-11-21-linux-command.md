---
title: linux 命令, linux command
author: w1100n
type: post
date: 2011-11-21T04:51:03+00:00
url: /?p=1568
categories:
  - Linux
tags:
  - RedHat

---
### time
用来计算  某个程序的运行耗时

    time <command0>
    time dig

user：程序在 User space 执行的时间
sys：程序在 Kernel space 执行的时间



### cp
    # 强制覆盖
    cp -f


```bash
# 查看系统启动时间和运行时间
uptime
who -b
who -r

# Linux系统历史启动的时间
last reboot

w命令查看

# host命令是常用的分析域名查询工具，可以用来测试域名系统工作是否正常。
host wiloon.com

#pidof命令用于查找指定名称的进程的进程号id号。
pidof

#kill pid
pidof fcitx | xargs kill

```

http://man.linuxde.net/host


重启
  
reboot
  
shutdown -r now
  
init 6
  
关机
  
shutdown -h now
  
init 0
  
退出
  
init 3

启动X

init 5
  
start x


---

https://blog.csdn.net/q_l_s/article/details/54897684