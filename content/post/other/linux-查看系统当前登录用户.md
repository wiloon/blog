---
title: 'Linux 查看 用户, 当前登录用户,  登录日志'
author: "-"
date: 2015-08-27T05:31:56+00:00
url: /?p=8169
categories:
  - Uncategorized
tags:
  - linux

---
## 'Linux 查看 用户, 当前登录用户,  登录日志'
/etc/shadow和/etc/passwd系统存在的所有用户名

more /var/log/secure
  
who /var/log/wtmp
  
干了些什么？
  
root账户下输入su - username
  
切换到username下输入
  
history
  
能看到这个用户历史命令,默认最近的1000条

http://blog.csdn.net/wudiyi815/article/details/8061459

作为系统管理员,你可能经常会 (在某个时候) 需要查看系统中有哪些用户正在活动。有些时候,你甚至需要知道他 (她) 们正在做什么。本文为我们总结了4种查看系统用户信息 (通过编号 (ID) ) 的方法。

  1. 使用w命令查看登录用户正在使用的进程信息

w命令用于显示已经登录系统的用户的名称,以及他们正在做的事。该命令所使用的信息来源于/var/run/utmp文件。w命令输出的信息包括: 

用户名称
  
用户的机器名称或tty号
  
远程主机地址
  
用户登录系统的时间
  
空闲时间 (作用不大) 
  
附加到tty (终端) 的进程所用的时间 (JCPU时间) 
  
当前进程所用时间 (PCPU时间) 
  
用户当前正在使用的命令
  
w命令还可以使用以下选项

-h忽略头文件信息
  
-u显示结果的加载时间
  
-s不显示JCPU, PCPU, 登录时间
  
$ w
  
23:04:27 up 29 days, 7:51, 3 users, load average: 0.04, 0.06, 0.02
  
USER TTY FROM LOGIN@ IDLE JCPU PCPU WHAT
  
ramesh pts/0 dev-db-server 22:57 8.00s 0.05s 0.01s sshd: ramesh [priv]
  
jason pts/1 dev-db-server 23:01 2:53 0.01s 0.01s -bash
  
john pts/2 dev-db-server 23:04 0.00s 0.00s 0.00s w

$ w -h
  
ramesh pts/0 dev-db-server 22:57 17:43 2.52s 0.01s sshd: ramesh [priv]
  
jason pts/1 dev-db-server 23:01 20:28 0.01s 0.01s -bash
  
john pts/2 dev-db-server 23:04 0.00s 0.03s 0.00s w -h

$ w -u
  
23:22:06 up 29 days, 8:08, 3 users, load average: 0.00, 0.00, 0.00
  
USER TTY FROM LOGIN@ IDLE JCPU PCPU WHAT
  
ramesh pts/0 dev-db-server 22:57 17:47 2.52s 2.49s top
  
jason pts/1 dev-db-server 23:01 20:32 0.01s 0.01s -bash
  
john pts/2 dev-db-server 23:04 0.00s 0.03s 0.00s w -u

$ w -s
  
23:22:10 up 29 days, 8:08, 3 users, load average: 0.00, 0.00, 0.00
  
USER TTY FROM IDLE WHAT
  
ramesh pts/0 dev-db-server 17:51 sshd: ramesh [priv]
  
jason pts/1 dev-db-server 20:36 -bash
  
john pts/2 dev-db-server 1.00s w -s

2.使用who命令查看 (登录) 用户名称及所启动的进程

who命令用于列举出当前已登录系统的用户名称。其输出为: 用户名、tty号、时间日期、主机地址。


$ who
  
ramesh pts/0 2009-03-28 22:57 (dev-db-server)
  
jason pts/1 2009-03-28 23:01 (dev-db-server)
  
john pts/2 2009-03-28 23:04 (dev-db-server)
  
如果只希望列出用户,可以使用如下语句: 


$ who | cut -d' ' -f1 | sort | uniq
  
john
  
jason
  
ramesh
  
补充: users命令,可用于打印输出登录服务器的用户名称。该命令除了有help和version选项外,再没有其他选项。如果某用户使用了多个终端,则相应的会显示多个重复的用户名。


$ users
  
john jason ramesh
  
3. 使用whoami命令查看你所使用的登录名称
  
whoami命令用于显示登入的用户名。


$ whoami
  
john
  
whoami命令的执行效果和id -un的效果完全一样,例如: 


$ id -un
  
john
  
whoami命令能显示当前登入的用户名称,以及当前所使用的tty信息。该命令的输出结果包括如下内容: 用户名、tty名、当前时间日期,同时还包括用户登录系统所使用的链接地址。


$ who am i
  
john pts/2 2009-03-28 23:04 (dev-db-server)

$ who mom likes
  
john pts/2 2009-03-28 23:04 (dev-db-server)

Warning: Don't try "who mom hates" command.
  
当然,如果你使用su命令改变用户,则该命令 (whoami) 所显示的结果将随之改变。
  
4. 随时查看系统的历史信息 (曾经使用过系统的用户信息) 
  
last命令可用于显示特定用户登录系统的历史记录。如果没有指定任何参数,则显示所有用户的历史信息。在默认情况下,这些信息 (所显示的信息) 将来源于/var/log/wtmp文件。该命令的输出结果包含以下几列信息: 

用户名称
  
tty设备号
  
历史登录时间日期
  
登出时间日期
  
总工作时间
  
$ last jason
  
jason pts/0 dev-db-server Fri Mar 27 22:57 still logged in
  
jason pts/0 dev-db-server Fri Mar 27 22:09 - 22:54 (00:45)
  
jason pts/0 dev-db-server Wed Mar 25 19:58 - 22:26 (02:28)
  
jason pts/1 dev-db-server Mon Mar 16 20:10 - 21:44 (01:33)
  
jason pts/0 192.168.201.11 Fri Mar 13 08:35 - 16:46 (08:11)
  
jason pts/1 192.168.201.12 Thu Mar 12 09:03 - 09:19 (00:15)
  
jason pts/0 dev-db-server Wed Mar 11 20:11 - 20:50 (00:39

转自: http://blog.csdn.net/newdriver2783/article/details/8059368