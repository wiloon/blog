---
title: kill, killall, signal
author: "-"
date: 2015-09-17T07:24:41+00:00
url: /?p=8289

categories:
  - inbox
tags:
  - reprint
---
## kill, killall, signal

### killall 命令
killall命令杀死同一进程组内的所有进程。其允许指定要终止的进程的名称，而非PID。
  
    killall java

http://www.cnblogs.com/itech/archive/2012/03/05/2380794.html

kill命令用于终止指定的进程（terminate a process) ，是Unix/Linux下进程管理的常用命令。通常，我们在需要终止某个或某些进程时，先使用ps/pidof/pstree/top等工具获取进程PID，然后使用kill命令来杀掉该进程。kill命令的另外一个用途就是向指定的进程或进程组发送信号（The  command kill sends the specified signal to the specified process or process group) ，或者确定进程号为PID的进程是否还在。比如，有许多程序都把SIGHUP信号作为重新读取配置文件的触发条件。
  
一 常用参数
  
格式: kill <pid>
  
格式: kill -TERM <pid>
  
发送SIGTERM信号到指定进程，如果进程没有捕获该信号，则进程终止（If no signal is specified, the TERM signal is sent.  The TERM signal will kill processes which do not catch this signal.) 

格式: kill -l
  
列出所有信号名称（Print a list of signal names.  These are found in /usr/include/linux/signal.h) 。只有第9种信号(SIGKILL)才可以无条件终止进程，其他信号进程都有权利忽略。下面是常用的信号: 

HUP    1    终端断线
INT    2    中断（同 Ctrl + C) 
QUIT   3    退出（同 Ctrl + \) 
TERM   15   终止
KILL   9    强制终止
CONT   18   继续（与STOP相反， fg/bg命令) 
STOP   19   暂停（同 Ctrl + Z) 

格式: kill -l <signame>
显示指定信号的数值。

格式: kill -9 <pid>
格式: kill -KILL <pid>
强制杀掉指定进程，无条件终止指定进程。

格式: kill %<jobid>
格式: kill -9 %<jobid>
杀掉指定的任务（使用jobs命令可以列出) 

格式: kill -QUIT <pid>

格式: kill -3 <pid>

使得程序正常的退出。


二 示例

1) 先用ps查找进程，然后用kill杀掉。
  
[root@new55 ~]# ps -ef|grep vim
  
root      3368  2884  0 16:21 pts/1    00:00:00 vim install.log
  
root      3370  2822  0 16:21 pts/0    00:00:00 grep vim
  
[root@new55 ~]# kill 3368
  
[root@new55 ~]# kill 3368
  
-bash: kill: (3368) - 没有那个进程

2) init进程是不可杀的。
  
参考: 
  
http://codingstandards.iteye.com/blog/847299
  
完！

作者: iTech
  
出处: http://itech.cnblogs.com/



```bash
kill -HUP xxx
ps -A | grep httpd | grep -v grep | awk '{ print $1; }' | xargs -L 1 sudo kill -HUP 
```

kill 命令

用于终止指定的进程（terminate a process) ，是 Unix/Linux 下进程管理的常用命令。

用途

通常在需要终止某个或某些进程时，先使用 ps/pidof/pstree/top 等工具获取进程 pid，然后用 kill 杀掉进程。
  
向指定的进程或进程组发送信号（The command kill sends the specified signal to the specified process or process group) ，或者确定进程号为 pid 的进程是否还在。例如，许多程序都把 HUP 信号作为重新读取配置文件的触发条件。
  
命令格式

kill <pid> kill -TERM <pid> 发送 TERM 信号到指定进程，如果进程没有捕获该信号，则进程终止（If no signal is specified, the TERM signal is sent. The TERM signal will kill processes which do not catch this signal.) 

kill -l

列出所有信号名称（Print a list of signal names. These are found in /usr/include/linux/signal.h) 。只有第9种信号(SIGKILL)才可以无条件终止进程，其他信号进程都有权利忽略。

作者: cityhash123
  
链接: http://www.jianshu.com/p/966d18eac17e
  
來源: 简书
  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

经过搜集和整理相关的linux杀死进程的材料，在这里本人给大家推荐本篇文章，希望大家看后会有不少收获。

  1. kill
  
    作用: 根据进程号杀死进程
  
    用法:  kill ［信号代码］ 进程ID
  
    举例: 
  
    [root@localhost ~]# ps auxf |grep httpd
  
    注意: kill -9 来强制终止退出
  
    举例 [root@localhost ~]# ps aux |grep gaim
  
    或者 [root@localhost ~]# pgrep -l gaim 5031 gaim
  
    5031 gaim
  
    [root@localhost ~]# kill -9 5031
  
    特殊用法: 
  
    kill -STOP [pid]
  
    发送SIGSTOP (17,19,23)停止一个进程，而并不linux杀死进程。
  
    kill -CONT [pid]
  
    发送SIGCONT (19,18,25)重新开始一个停止的进程。
  
    kill -KILL [pid]
  
    发送SIGKILL (9)强迫进程立即停止，并且不实施清理操作。
  
    kill -9 -1
  
    终止你拥有的全部进程。 
### killall
作用: 通过程序的名字，直接杀死所有进程  
用法: killall 正在运行的程序名  
举例: 

    pgrep -l gaim 2979 gaim
    killall gaim
  
注意: 该命令可以使用 -9 参数来强制杀死进程

### pkill
  
    作用: 通过程序的名字，直接杀死所有进程
  
    用法: #pkill 正在运行的程序名
  
    举例: 
  
    [root@localhost beinan]# pgrep -l gaim 2979 gaim
  
    [root@localhost beinan]# pkill gaim

  4. xkill
  
    作用: 杀死桌面图形界面的程序。
  
    应用情形实例: firefox出现崩溃不能退出时，点鼠标就能杀死firefox 。
  
    当xkill运行时出来和个人脑骨的图标，哪个图形程序崩溃一点就OK了。
  
    如果您想终止xkill ，就按右键取消；
  
    调用方法: 
  
    [root@localhost ~]# xkill

◆注: 
  
KILLALL
  
NAME (名称)
  
killall - 以名字方式来linux杀死进程
  
SYNOPSIS (总览)
  
killall [-egiqvw] [-signal] name ...
  
killall -l
  
killall -V
  
DESCRIPTION (描述)
  
killall 发送一条信号给所有运行任意指定命令的进程. 如果没有指定信号名, 则发送SIGTERM.。
  
信号可以以名字 (如 -HUP ) 或者数字 (如 -1 ) 的方式指定. 信号 0 (检查进程是否存在)只能以数字方式指定。
  
如果命令名包括斜杠 (/), 那么执行该特定文件的进程将被杀掉, 这与进程名无关。
  
如果对于所列命令无进程可杀, 那么 killall 会返回非零值. 如果对于每条命令至少杀死了一个进程, killall 返回 0。Killall 进程决不会杀死自己 (但是可以杀死其它 killall 进程)。

OPTIONS (选项)

-e对于很长的名字, 要求准确匹配. 如果一个命令名长于 15 个字符, 则可能不能用整个名字 (溢出了). 在这种情况下, killall 会杀死所有匹配名字前 15 个字符的所有进程. 有了 -e 选项,这样的记录将忽略. 如果同时指定了 -v 选项, killall 会针对每个忽略的记录打印一条消息。

-g杀死属于该进程组的进程. kill 信号给每个组只发送一次, 即使同一进程组中包含多个进程。

-i交互方式，在linux杀死进程之前征求确认信息。

-l列出所有已知的信号名。

-q如果没有进程杀死, 不会提出抱怨。

-v报告信号是否成功发送。

-V显示版本信息。

-w等待所有杀的进程死去. killall 会每秒检查一次是否任何被杀的进程仍然存在, 仅当都死光后才返回. 注意: 如果信号被忽略或没有起作用, 或者进程停留在僵尸状态, killall 可能会永久等待。

FILES(相关文件)
  
/proc proc文件系统的存在位置。
  
KNOWN bugS (已知 BUGS)
  
以文件方式杀死只对那些在执行时一直打开的可执行文件起作用, 也即, 混杂的可执行文件不能够通过这种方式杀死。
  
要警告的是输入 killall name 可能不会在非 Linux 系统上产生预期的效果, 特别是特权用户执行时要小心。
  
在两次扫描的间隙, 如果进程消失了而被代之以一个有同样 PID 的新进程, killall -w 侦测不到。

http://os.51cto.com/art/200910/158639.htm

根据进程名杀死进程 －kill进程名
  
#pkill 进程名
  
或是
  
#killall 进程名
  
的确这个两个命令都能做到这些，而且我们平时一般知道进程名需要杀死进程的时候也都是用的这两个命令。可是他叫我用kill 命令来完成这个一操作。我们知道kill 要杀死进程是需要知道进程的id的即进程号，其实这个思路就是需要通过其他命令获取相应进程的进程号，然后用kill 杀掉。
  
这里提供两个方法: 
  
1. #kill -9 $(ps -ef|grep 进程名关键字|gawk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')这个是利用管道和替换将 进程名对应的进程号提出来作为kill的参数。
  
很显然上面的方法能完成但是过于复杂，下面这种就显得简单的多了
  
2. #kill -9 $(pidof 进程名关键字)

https://blog.csdn.net/zhaoyue007101/article/details/7699259

