---
title: linux shell sleep,wait
author: "-"
date: 2011-05-01T05:34:13+00:00
url: /?p=159
categories:
  - Linux

tags:
  - reprint
---
## linux shell sleep,wait

sleep 5
  
等待 秒

一、启动后台子任务

        在执行命令后加&操作符，表示将命令放在子shell中异步执行。可以达到多线程效果。如下，

     sleep 10 #等待10秒，再继续下一操作
     sleep 10 & #当前shell不等待，后台子shell等待
    

二、wait命令介绍

        wait  [作业指示或进程号]

        1.等待作业号或者进程号制定的进程退出，返回最后一个作业或进程的退出状态状态。如果没有制定参数，则等待所有子进程的退出，其退出状态为0.

        2.如果是shell中等待使用wait，则不会等待调用函数中子任务。在函数中使用wait，则只等待函数中启动的后台子任务。

        3.在shell中使用wait命令，相当于高级语言里的多线程同步。

三、例子

1.使用wait等待所有子任务结束。

#!/bin/bash
  
sleep 10 &
  
sleep 5&
  
wait #等待10秒后，退出
  
#!/bin/bash
  
sleep 10 &
  
sleep 5&
  
wait $! #$!表示上个子进程的进程号，wait等待一个子进程，等待5秒后，退出

2.在函数中使用wait

#!/bin/bash
  
source ~/.bashrc

fun(){
      
echo "fun is begin.timeNum:$timeNum"
      
local timeNum=$1
      
sleep $timeNum &
      
wait #这个只等待wait前面sleep

    echo "fun is end.timeNum:$timeNum"
    

}

fun 10 &
  
fun 20 &

wait #如果fun里面没有wait，则整个脚本立刻退出，不会等待fun里面的sleep
  
echo "all is ending"
  
输出结果为: 

fun is begin.timeNum:10
  
fun is begin.timeNum:20
  
fun is end.timeNum:10
  
fun is end.timeNum:20
  
all is ending

从输出结果，可以看到，整个脚本，等待了所有子任务的退出
  
————————————————
  
版权声明: 本文为CSDN博主「雙湖之梦」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/shuanghujushi/article/details/38186303