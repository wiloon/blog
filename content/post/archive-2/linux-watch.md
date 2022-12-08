---
title: watch command
author: "-"
date: 2017-08-08T07:32:15+00:00
url: watch
categories:
  - inbox
tags:
  - reprint
---
## watch command

watch可以周期性的执行一个程序,并显示执行结果。

```bash
watch -d netstat -ant
watch -n 3 -d netstat -ant
```

### 命令参数

* -n, -interval, watch 默认每两秒运行一下程序, 可以用 -n或-interval来指定间隔的时间。
* -d, -differences 用-d或-differences 选项watch 会高亮显示变化的区域。 而-d=cumulative选项会把变动过的地方(不管最近的那次有没有变动)都高亮显示出来。
* -t, -no-title 会关闭watch命令在顶部的时间间隔,命令,当前时间的输出。
* -h, -help 查看帮助文档

watch是一个非常实用的命令,基本所有的Linux发行版都带有这个小工具,如同名字一样,watch可以帮你监测一个命令的运行结果,省得你一遍遍的手动运行。在Linux下,watch是周期性的执行下个程序,并全屏显示执行结果。你可以拿他来监测你想要的一切命令的结果变化,比如 tail 一个 log 文件,ls 监测某个文件的大小变化,看你的想象力了！
  
1．命令格式:
  
```bash
watch[参数][命令]
```
  
2．命令功能:
  
可以将命令的输出结果输出到标准输出设备,多用于周期性执行命令/定时执行命令

4．使用实例:
  
实例1:
  
命令: 每隔一秒高亮显示网络链接数的变化情况
  
watch -n 1 -d netstat -ant
  
说明:
  
其它操作:
  
切换终端:  Ctrl+x
  
退出watch: Ctrl+g
  
实例2: 每隔一秒高亮显示http链接数的变化情况
  
命令:
  
watch -n 1 -d 'pstree|grep http'
  
说明:
  
每隔一秒高亮显示http链接数的变化情况。 后面接的命令若带有管道符,需要加"将命令区域归整。
  
实例3: 实时查看模拟攻击客户机建立起来的连接数
  
命令:
  
watch 'netstat -an | grep:21 | \ grep<模拟攻击客户机的IP>| wc -l'
  
说明:
  
实例4: 监测当前目录中 scf' 的文件的变化
  
命令:
  
watch -d 'ls -l|grep scf'
  
实例5: 10秒一次输出系统的平均负载
  
命令:
  
watch -n 10 'cat /proc/loadavg'
