---
title: cpustat
author: "-"
date: 2017-05-04T07:47:46+00:00
url: /?p=10208
categories:
  - Uncategorized

tags:
  - reprint
---
## cpustat
cpustat 是 Linux 下一个强大的系统性能测量程序,它用 Go 编程语言[1] 编写。它通过使用 "用于分析任意系统的性能的方法（USE) [2]",以有效的方式显示 CPU 利用率和饱和度。

它高频率对系统中运行的每个进程进行取样,然后以较低的频率汇总这些样本。例如,它能够每 200ms 测量一次每个进程,然后每 5 秒汇总这些样本,包括某些度量的最小/平均/最大值（min/avg/max) 。

go get github.com/uber-common/cpustat

sudo $GOBIN/cpustat -u root -t

https://linux.cn/article-8466-1.html