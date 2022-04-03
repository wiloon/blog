---
title: "taskset"
author: "-"
date: "2021-07-06 06:42:56"
url: "taskset"
categories:
  - inbox
tags:
  - inbox
---
## "taskset"
一、在Linux上修改进程的“CPU亲和力”

在Linux上，可以通过 taskset 命令进行修改。以Ubuntu为例，运行如下命令可以安装taskset工具。

# apt-get install schedutils
对运行中的进程，文档上说可以用下面的命令，把CPU#1 #2 #3分配给PID为2345的进程: 

# taskset -cp 1,2,3 2345
但我尝试没奏效，于是我关掉了MySQL，并用taskset将它启动: 

# taskset -c 1,2,3 /etc/init.d/MySQL start
对于其他进程，也可如此处理 (nginx除外，详见下文) 。之后用top查看CPU的使用情况，原来空闲的#1 #2 #3，已经在辛勤工作了。





二、配置nginx绑定CPU

刚才说nginx除外，是因为nginx提供了更精确的控制。

在conf/nginx.conf中，有如下一行: 

worker_processes  1;
这是用来配置nginx启动几个工作进程的，默认为1。而nginx还支持一个名为worker_cpu_affinity的配置项，也就是说，nginx可以为每个工作进程绑定CPU。我做了如下配置: 

worker_processes  3;
worker_cpu_affinity 0010 0100 1000;
这里0010 0100 1000是掩码，分别代表第2、3、4颗cpu核心。

重启nginx后，3个工作进程就可以各自用各自的CPU了。



三、刨根问底

如果自己写代码，要把进程绑定到CPU，该怎么做？可以用sched_setaffinity函数。在Linux上，这会触发一次系统调用。
如果父进程设置了affinity，之后其创建的子进程是否会有同样的属性？我发现子进程确实继承了父进程的affinity属性。


四、Windows？

在Windows上修改“CPU亲和力”，可以通过任务管理器搞定。





* 个人感觉，Windows系统中翻译的“处理器关系”比“CPU亲和力”容易理解点儿

—————–

进行了这样的修改后，即使系统负载达到3以上，不带缓存打开blogkid.net首页 (有40多次查询) 依然顺畅；以前一旦负载超过了1.5，响应就很慢了。效果很明显。

 

linux taskset命令详解

SYNOPSIS
       taskset [options] [mask | list ] [pid | command [arg]...]
OPTIONS
       -p, --pid
              operate on an existing PID and not launch a new task
       -c, --cpu-list
              specifiy  a  numerical  list of processors instead of a bitmask.
              The list may contain multiple items,  separated  by  comma,  and
              ranges.  For example, 0,5,7,9-11.
       -h, --help
              display usage information and exit
       -V, --version
              output version information and exit