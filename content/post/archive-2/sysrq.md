---
title: SysRq
author: "-"
date: 2018-08-27T08:53:47+00:00
url: SysRq
categories:
  - Linux
tags:
  - reprint
---
## SysRq

https://blog.csdn.net/jasonchen_gbd/article/details/79080576

SysRq是Linux提供的一个"Magic System Request Key", 它可以在系统出现故障的时候协助恢复和调试系统。只要你的虚拟终端或串口还可以接收键盘输入 (系统还能响应键盘的按键中断), SysRq 就可用, 你可以借助它来查看当时的内存、进程状态等信息,而不是直接强行拔掉电源重启系统。

SysRq能做的事情看HELP就知道了: 

SysRq : HELP : loglevel(0-9) reboot(b) crash(c) terminate-all-tasks(e) memory-full-oom-kill(f)
  
kill-all-tasks(i) thaw-filesystems(j) sak(k) show-backtrace-all-active-cpus(l)
  
show-memory-usage(m) nice-all-RT-tasks(n) poweroff(o) show-registers(p) show-all-timers(q)
  
unraw(r) sync(s) show-task-states(t) unmount(u) show-blocked-tasks(w) dump-ftrace-buffer(z)
  
## SysRq的用法
  
2.1 启用SysRq
  
首先要确保内核打开了CONFIG_MAGIC_SYSRQ配置项,这样SysRq的底层处理才可用。
  
另外内核中有一个宏定义SYSRQ_DEFAULT_ENABLE,表示系统默认情况下是否启用SysRq功能键。当然,不管这个值是不是yes,你都可以通过proc文件系统来开启或关闭SysRq键: 
  
查看当前SysRq是否被开启 (0表示关闭), archlinux 默认开启 

`cat /proc/sys/kernel/sysrq`

开启SysRq: 

# echo 1 > /proc/sys/kernel/sysrq

也可以使用sysctl命令: 

# sysctl -w kernel.sysrq=1

kernel.sysrq = 1
  
实际上sysctl这条命令就是通过修改/proc/sys/kernel/sysrq来生效的。可以把"kernel.sysrq = 1"设置到/etc/sysctl.conf中,使SysRq在下次系统重启仍生效。

上面说0表示完全关闭SysRq,1表示使能SysRq的所有功能,还可以设置成其他数字来选择开启部分功能,可参考内核里的Documentation/sysrq.txt。
  
SysRq支持的所有功能列表及相应的handler见drivers/tty/sysrq.c中静态数组sysrq_key_table[]的定义,当然,也可以通过下面提到的SysRq的help信息了解到。

2.2 使用SysRq
  
我们可以直接通过按键的方式或者通过写/proc/sysrq-trigger的方式来触发SysRq的操作。SysRq支持的操作可参考下面的HELP输出: 

# echo > /proc/sysrq-trigger

[16037.132214] SysRq : HELP : loglevel(0-9) reboot(b) crash(c) terminate-all-tasks(e) memory-full-oom-kill(f) kill-all-tasks(i) thaw-filesystems(j) sak(k) show-backtrace-all-active-cpus(l) show-memory-usage(m) nice-all-RT-tasks(n) poweroff(o) show-registers(p) show-all-timers(q) unraw(r) sync(s) show-task-states(t) unmount(u) show-blocked-tasks(w) dump-ftrace-buffer(z)
  
即, "SysRq键+一个字母" 来触发一个操作,例如 SysRq + t 打印所有任务的状态。

那么如何产生一个SysRq键呢？

在Ubuntu下,图形界面环境不能使用SysRq,需进入文本虚拟终端环境 (Ctrl+Alt+F1从图形桌面切换到虚拟终端,Alt+F7可切回来) ,然后同时按下Alt和Print Screen键以及相应的字母键。
  
在嵌入式设备上, 通过串口工具也可以触发 SysRq, 如果使用 SecureCRT, 则同时按下 Alt 和 Print Screen 键, 会出现上述HELP,然后紧接着按下某个字母。如果使用teraTerm,则点击菜单中的Control->Send Break,会出现上述HELP,然后紧接着按下某个字母。
  
也可以不通过按键,而是写/proc/sysrq-trigger的方式,用法形如: 

echo c > /proc/sysrq-trigger
  
即,向sysrq-trigger写入相应的字母即可。并且,无论/proc/sys/kernel/sysrq是什么值,这种方式都是可用的。

  1. SysRq有什么用
  
    从上述HELP信息就能看出来SysRq都能干什么,在Documentation/sysrq.txt中也有详细介绍。例如,在系统卡住或出现其他异常但还没完全死掉 (没有panic或触发watchdog) 时,可以人为地制造OOM或panic,看看当前内核在干什么。下面这篇文章对SysRq的使用场景有较全面的介绍和举例,贴在这里供参考: 
  
    https://www.ibm.com/developerworks/cn/linux/l-cn-sysrq/

我上面提到了sysrq的handlers定义的代码位置,如果需要,你甚至可以添加自定义的操作。