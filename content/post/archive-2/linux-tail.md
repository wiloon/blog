---
title: tail
author: "-"
date: 2016-08-14T15:41:25+00:00
url: tail
categories:
  - Linux
tags:
  - reprint
  - Command
---
## tail

## 同时监控多个日志文件

```bash
tail -f foo.log bar.log
tail -f *.log
```

Linux监测日志tail命令详细使用
如果在Linux下调试程序的朋友应该都知道tail命令,它确实是调试程序监测日志文件的能手。打开Linux输入以下命令看看命令的使用帮助

[root@lee ~]# tail --help
用法: tail [选项]... [文件]...
显示每个指定文件的最后10 行到标准输出。
若指定了多于一个文件,程序会在每段输出的开始添加相应文件名作为头。
如果不指定文件或文件为"-" ,则从标准输入读取数据。

长选项必须使用的参数对于短选项时也是必需使用的。
  -c, --bytes=K         输出最后K 字节；另外,使用-c +K 从每个文件的
                        第K 字节输出
  -f, --follow[={name|descriptor}]
                即时输出文件变化后追加的数据。
                        -f, --follow 等于--follow=descriptor
  -F            即--follow=name --retry
  -n, --lines=K            output the last K lines, instead of the last 10;
                           or use -n +K to output lines starting with the Kth
      --max-unchanged-stats=N
                           with --follow=name, reopen a FILE which has not
                           changed size after N (default 5) iterations
                           to see if it has been unlinked or renamed
                           (this is the usual case of rotated log files).
                           With inotify, this option is rarely useful.
      --pid=PID         同 -f 一起使用,当 PID 所对应的进程死去后终止
  -q, --quiet, --silent 不输出给出文件名的头
      --retry           即使目标文件不可访问依然试图打开；在与参数
                        --follow=name 同时使用时常常有用。
  -s, --sleep-interval=N   with -f, sleep for approximately N seconds
                             (default 1.0) between iterations.
                           With inotify and --pid=P, check process P at
                           least once every N seconds.
  -v, --verbose            always output headers giving file names
      --help            显示此帮助信息并退出
      --version         显示版本信息并退出

如果字节数或行数K 的第一个字符是"+",输出从文件开始第K 个项目,否则输出文件
最后K 个项目。K 可以使用一下几种单位之一:
b 512,kB 1000,K 1024,MB 1000*1000,M 1024*1024,
GB 1000*1000*1000,G 1024*1024*1024,以及T,P,E,Z,Y。

如果您希望即时追查一个文件的有效名称而非描述内容(例如循环日志),默认
的程序动作并不如您所愿。在这种场合可以使用--follow=name 选项,它会使
tail 定期追踪打开给定名称的文件,以确认它是否被删除或被其它某些程序重新创建过。

请向bug-coreutils@gnu.org 报告tail 的错误
GNU coreutils 项目主页: [http://www.gnu.org/software/coreutils/](http://www.gnu.org/software/coreutils/)
GNU 软件一般性帮助: [http://www.gnu.org/gethelp/](http://www.gnu.org/gethelp/)
请向[http://translationproject.org/team/zh_CN.html](http://translationproject.org/team/zh_CN.html) 报告tail 的翻译错误
要获取完整文档,请运行: info coreutils 'tail invocation'

---

[https://www.qttc.net/311-linux-tail.html](https://www.qttc.net/311-linux-tail.html)

[https://blog.csdn.net/weixin_41585557/article/details/82724381](https://blog.csdn.net/weixin_41585557/article/details/82724381)
