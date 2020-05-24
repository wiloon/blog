---
title: linux commands
author: wiloon
type: post
date: 2017-12-17T05:52:33+00:00
url: /?p=11621
categories:
  - Uncategorized

---
```bash# 查看系统启动时间和运行时间
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