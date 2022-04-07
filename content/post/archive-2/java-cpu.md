---
title: Java cpu占用调查
author: "-"
date: 2015-12-23T01:44:52+00:00
url: /?p=8587
categories:
  - Uncategorized

tags:
  - reprint
---
## Java cpu占用调查

### 获取Java进程的PID

```bash
jcmd -l
```
### 查看对应进程的哪个线程占用CPU过高.
```bash
top -H -p <PID>
ps -mp <PID> -o THREAD,tid,time | sort -rn | head -n 10
```

### 打印进程的堆栈信息
```bash
jcmd <PID> Thread.print > stack.txt
# 或
jstack <PID> stack.txt
```

#### 将线程的PID转换为16进制。
```bash
echo "obase=16; PID" | bc
printf "%x\n" 73658
```

### 在第二步导出的 stack.txt 中查找转换成为16进制的线程PID。找到对应的线程栈。

    分析负载高的线程栈都是什么业务操作。优化程序并处理问题。


SystemTap,LatencyTOP,vmstat, sar, iostat, top, tcpdump
  
iftop, iptraf, ntop, tcpdump
  
Java的JProfiler/TPTP/CodePro Profiler


  
    性能调优攻略
  


https://coolshell.cn/articles/7490.html/embed#?secret=sGuaIXdcl5
  
<https://www.linuxhot.com/java-cpu-used-high.html>
  
<https://linux.cn/article-5633-1.html>