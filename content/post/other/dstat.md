---
title: dstat
author: "-"
date: 2012-11-13T13:33:43+00:00
url: dstat
categories:
  - Linux
tags:
  - reprint
---
## dstat

dstat 是一个可以取代vmstat，iostat，netstat和ifstat这些命令的多功能产品。dstat克服了这些命令的局限并增加了一些另外的功能，增加了监控项，也变得更灵活了。dstat可以很方便监控系统运行状况并用于基准测试和排除故障。

dstat可以让你实时地看到所有系统资源，例如，你能够通过统计IDE控制器当前状态来比较磁盘利用率，或者直接通过网络带宽数值来比较磁盘的吞吐率（在相同的时间间隔内）。

dstat将以列表的形式为你提供选项信息并清晰地告诉你是在何种幅度和单位显示输出。这样更好地避免了信息混乱和误报。更重要的是，它可以让你更容易编写插件来收集你想要的数据信息，以从未有过的方式进行扩展。

Dstat的默认输出是专门为人们实时查看而设计的，不过你也可以将详细信息通过CSV输出到一个文件，并导入到Gnumeric或者Excel生成表格中。
>https://linux.cn/article-3215-1.html


```bash
pacman -S dstat
```