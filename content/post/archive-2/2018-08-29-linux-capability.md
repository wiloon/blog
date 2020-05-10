---
title: Linux capability
author: wiloon
type: post
date: 2018-08-29T07:06:54+00:00
url: /?p=12608
categories:
  - Uncategorized

---
http://www.cnblogs.com/iamfy/archive/2012/09/20/2694977.html

一)概述:
  
1)从2.1版开始,Linux内核有了能力(capability)的概念,即它打破了UNIX/LINUX操作系统中超级用户/普通用户的概念,由普通用户也可以做只有超级用户可以完成的工作.
  
2)capability可以作用在进程上(受限),也可以作用在程序文件上,它与sudo不同,sudo只针对用户/程序/文件的概述,即sudo可以配置某个用户可以执行某个命令,可以更改某个文件,而capability是让某个程序拥有某种能力,例如:
  
capability让/tmp/testkill程序可以kill掉其它进程,但它不能mount设备节点到目录,也不能重启系统,因为我们只指定了它kill的能力,即使程序有问题也不会超出能力范围.
  
3)每个进程有三个和能力有关的位图:inheritable(I),permitted(P)和effective(E),对应进程描述符task\_struct(include/linux/sched.h)里面的cap\_effective, cap\_inheritable, cap\_permitted,所以我们可以查看/proc/PID/status来查看进程的能力.
  
4)cap\_effective:当一个进程要进行某个特权操作时,操作系统会检查cap\_effective的对应位是否有效,而不再是检查进程的有效UID是否为0.
  
例如,如果一个进程要设置系统的时钟,Linux的内核就会检查cap\_effective的CAP\_SYS_TIME位(第25位)是否有效.
  
5)cap\_permitted:表示进程能够使用的能力,在cap\_permitted中可以包含cap\_effective中没有的能力，这些能力是被进程自己临时放弃的,也可以说cap\_effective是cap_permitted的一个子集.
  
6)cap_inheritable:表示能够被当前进程执行的程序继承的能力.