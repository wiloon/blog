---
title: golang 程序 too many open files
author: "-"
date: 2015-09-02T00:49:30+00:00
url: go/ulimit
categories:
  - Go
tags:
  - original

---
## golang 程序 too many open files

Go 程序  报错  too many open files

程序 报错之后 查看 进程 打开的 文件  lsof -p 14092 |wc -l,  1032

排除掉 内存映射文件(mem), 列标题, cwd, rtd, txt, 刚好 1024,  lsof -p 14092 看到打开的 fd 最大值  1023u

shell 下
查看系统的文件数设置

ulimit -a
ulimit -Hn
ulimit -Sn
65535

### systemd limit

[https://unix.stackexchange.com/questions/345595/how-to-set-ulimits-on-service-with-systemd](https://unix.stackexchange.com/questions/345595/how-to-set-ulimits-on-service-with-systemd)

### Go rlimit

[https://stackoverflow.com/questions/17817204/how-to-set-ulimit-n-from-a-golang-program](https://stackoverflow.com/questions/17817204/how-to-set-ulimit-n-from-a-golang-program)

>wangyue.dev/lsof
>wangyue.dev/ulimit
>wangyue.dev/systemd/script
