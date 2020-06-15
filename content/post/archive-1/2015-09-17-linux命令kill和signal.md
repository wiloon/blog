---
title: Linux命令kill和signal
author: wiloon
type: post
date: 2015-09-17T07:24:41+00:00
url: /?p=8289
categories:
  - Uncategorized

---
http://www.cnblogs.com/itech/archive/2012/03/05/2380794.html

kill命令用于终止指定的进程（terminate a process），是Unix/Linux下进程管理的常用命令。通常，我们在需要终止某个或某些进程时，先使用ps/pidof/pstree/top等工具获取进程PID，然后使用kill命令来杀掉该进程。kill命令的另外一个用途就是向指定的进程或进程组发送信号（The  command kill sends the specified signal to the specified process or process group），或者确定进程号为PID的进程是否还在。比如，有许多程序都把SIGHUP信号作为重新读取配置文件的触发条件。
  
一 常用参数
  
格式：kill <pid>
  
格式：kill -TERM <pid>
  
发送SIGTERM信号到指定进程，如果进程没有捕获该信号，则进程终止（If no signal is specified, the TERM signal is sent.  The TERM signal will kill processes which do not catch this signal.）

格式：kill -l
  
列出所有信号名称（Print a list of signal names.  These are found in /usr/include/linux/signal.h）。只有第9种信号(SIGKILL)才可以无条件终止进程，其他信号进程都有权利忽略。下面是常用的信号：
  
HUP     1    终端断线
  
INT       2    中断（同 Ctrl + C）
  
QUIT    3    退出（同 Ctrl + \）
  
TERM    15    终止
  
KILL      9    强制终止
  
CONT   18    继续（与STOP相反， fg/bg命令）
  
STOP    19    暂停（同 Ctrl + Z）

格式：kill -l <signame>
  
显示指定信号的数值。

格式：kill -9 <pid>
  
格式：kill -KILL <pid>
  
强制杀掉指定进程，无条件终止指定进程。

格式：kill %<jobid>
  
格式：kill -9 %<jobid>
  
杀掉指定的任务（使用jobs命令可以列出）

格式：kill -QUIT <pid>
  
格式：kill -3 <pid>
  
使得程序正常的退出。

killall命令
  
killall命令杀死同一进程组内的所有进程。其允许指定要终止的进程的名称，而非PID。
  
\# killall httpd

二 示例

1）先用ps查找进程，然后用kill杀掉。
  
[root@new55 ~]# ps -ef|grep vim
  
root      3368  2884  0 16:21 pts/1    00:00:00 vim install.log
  
root      3370  2822  0 16:21 pts/0    00:00:00 grep vim
  
[root@new55 ~]# kill 3368
  
[root@new55 ~]# kill 3368
  
-bash: kill: (3368) - 没有那个进程

2）init进程是不可杀的。

3）列出所有信号名称
  
[root@new55 ~]# kill -l
  
1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL
  
5) SIGTRAP      6) SIGABRT      7) SIGBUS       8) SIGFPE
  
9) SIGKILL     10) SIGUSR1     11) SIGSEGV     12) SIGUSR2
  
13) SIGPIPE     14) SIGALRM     15) SIGTERM     16) SIGSTKFLT
  
17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP
  
21) SIGTTIN     22) SIGTTOU     23) SIGURG      24) SIGXCPU
  
25) SIGXFSZ     26) SIGVTALRM   27) SIGPROF     28) SIGWINCH
  
29) SIGIO       30) SIGPWR      31) SIGSYS      34) SIGRTMIN
  
35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3  38) SIGRTMIN+4
  
39) SIGRTMIN+5  40) SIGRTMIN+6  41) SIGRTMIN+7  42) SIGRTMIN+8
  
43) SIGRTMIN+9  44) SIGRTMIN+10 45) SIGRTMIN+11 46) SIGRTMIN+12
  
47) SIGRTMIN+13 48) SIGRTMIN+14 49) SIGRTMIN+15 50) SIGRTMAX-14
  
51) SIGRTMAX-13 52) SIGRTMAX-12 53) SIGRTMAX-11 54) SIGRTMAX-10
  
55) SIGRTMAX-9  56) SIGRTMAX-8  57) SIGRTMAX-7  58) SIGRTMAX-6
  
59) SIGRTMAX-5  60) SIGRTMAX-4  61) SIGRTMAX-3  62) SIGRTMAX-2
  
63) SIGRTMAX-1  64) SIGRTMAX
  
[root@new55 ~]#
  
/usr/include/linux/signal.h 写道
  
#define SIGHUP 1
  
#define SIGINT 2
  
#define SIGQUIT 3
  
#define SIGILL 4
  
#define SIGTRAP 5
  
#define SIGABRT 6
  
#define SIGIOT 6
  
#define SIGBUS 7
  
#define SIGFPE 8
  
#define SIGKILL 9
  
#define SIGUSR1 10
  
#define SIGSEGV 11
  
#define SIGUSR2 12
  
#define SIGPIPE 13
  
#define SIGALRM 14
  
#define SIGTERM 15
  
#define SIGSTKFLT 16
  
#define SIGCHLD 17
  
#define SIGCONT 18
  
#define SIGSTOP 19
  
#define SIGTSTP 20
  
#define SIGTTIN 21
  
#define SIGTTOU 22
  
#define SIGURG 23
  
#define SIGXCPU 24
  
#define SIGXFSZ 25
  
#define SIGVTALRM 26
  
#define SIGPROF 27
  
#define SIGWINCH 28
  
#define SIGIO 29
  
#define SIGPOLL SIGIO
  
/*
  
#define SIGLOST 29
  
*/
  
#define SIGPWR 30
  
#define SIGSYS 31
  
#define SIGUNUSED 31

/\* These should not be considered constants from userland. \*/
  
#define SIGRTMIN 32
  
#define SIGRTMAX _NSIG

参考：
  
http://codingstandards.iteye.com/blog/847299
  
完！

作者：iTech
  
出处：http://itech.cnblogs.com/