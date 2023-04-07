---
title: systemtap
author: "-"
date: 2017-05-04T08:46:56+00:00
url: /?p=10210
categories:
  - Inbox
tags:
  - reprint
---
## systemtap

<http://www.cnblogs.com/hazir/p/systemtap_introduction.html>

内核探测工具systemtap简介
  
systemtap是内核开发者必须要掌握的一个工具,本文我将简单介绍一下此工具,后续将会有系列文章介绍systemtap的用法。

什么是systemtap
  
假如现在有这么一个需求: 需要获取正在运行的 Linux 系统的信息,如我想知道系统什么时候发生系统调用,发生的是什么系统调用等这些信息,有什么解决方案呢？

最原始的方法是,找到内核系统调用的代码,加上我们需要获得信息的代码、重新编译内核、安装、选择我们新编译的内核重启。这种做法对于内核开发人员简直是梦魇,因为一遍做下来至少得需要1个多小时,不仅破坏了原有内核代码,而且如果换了一个需求又得重新做一遍上面的工作。所以,这种调试内核的方法效率是极其底下的。
  
之后内核引入了一种Kprobe机制,可以用来动态地收集调试和性能信息的工具,是一种非破坏性的工具,用户可以用它跟踪运行中内核任何函数或执行的指令等。相比之前的做法已经有了质的提高了,但Kprobe并没有提供一种易用的框架,用户需要自己去写模块,然后安装,对用户的要求还是蛮高的。
  
systemtap 是利用Kprobe 提供的API来实现动态地监控和跟踪运行中的Linux内核的工具,相比Kprobe,systemtap更加简单,提供给用户简单的命令行接口,以及编写内核指令的脚本语言。对于开发人员,systemtap是一款难得的工具。
  
下面将会介绍systemtap的安装、systemtap的工作原理以及几个简单的示例。

systemtap 的安装
  
我的主机 Linux 发行版是32位 Ubuntu13.04,内核版本 3.8.0-30。由于 systemtap 运行需要内核的调试信息支撑,默认发行版的内核在配置时这些调试开关没有打开,所以安装完systemtap也是无法去探测内核信息的。 下面我以两种方式安装并运行 systemtap:

方法一

编译内核以支持systemtap
  
我们重新编译内核让其支持systemtap,首先你想让内核中有调试信息,编译内核时需要加上 -g 标志；其次,你还需要在配置内核时将 Kprobe 和 debugfs 开关打开。最终效果是,你能在内核 .config 文件中看到下面四个选项是设置的:

CONFIG_DEBUG_INFO

CONFIG_KPROBES

CONFIG_DEBUG_FS

CONFIG_RELAY
  
配置完之后,按照之前你编译内核的步骤编译即可。

获取systemtap源码
  
从此地址 <https://sourceware.org/systemtap/ftp/releases下载已经发布的systemtap>的源代码,截至目前 (2013.9.17) 最新版本为systemtap-2.3。下载完之后解压。 当然你还可以使用 git 去克隆最新的版本 (2.4) ,命令如下:

git clone git://sources.redhat.com/git/systemtap.git
  
编译安装systemtap
  
如果你下载的是最新版本的systemtap,那么你需要新版的 elfutils,可以从<https://fedorahosted.org/releases/e/l/elfutils/> 下载elfutils-0.156 版本。下载之后解压缩到适合的目录 (我放在~/Document/ 下) ,不需要安装,只要配置systemtap时指定其位置即可。 进入之前解压systemtap的目录,使用下面命令进行配置:

./configure -with-elfutils=~/Document/elfutils-0.156
  
以这里方法配置之后,你只需要再运行 make install 即完成systemtap的编译安装。如果需要卸载的话,运行 make uninstall。

方法二

由于发行版的内核默认无内核调试信息,所以我们还需要一个调试内核镜像,在<http://ddebs.ubuntu.com/pool/main/l/linux/> 找到你的内核版本相对应的内核调试镜像 (版本号包括后面的发布次数、硬件体系等都必须一致) ,如针对我上面的内核版本,就可以用如下命令下载安装内核调试镜像:

$ wget <http://ddebs.ubuntu.com/pool/main/l/linux/linux-image-debug-3.8.0-30-generic_dbgsym_3.8.0-30.43_i386.ddeb>
  
$ sudo dpkg -i linux-image-debug-3.8.0-30-generic_dbgsym_3.8.0-30.43_i386.ddeb
  
一般这种方法下,你只需要使用apt在线安装systemtap即可:

$sudo apt-get install systemtap
  
当然方法二仅限于Ubuntu发行版,至于其他的发行版并不能照搬,网上也有很多相关的资料。

systemtap 测试示例
  
安装完systemtap之后,我们需要测试一下systemtap是否能正确运行:

示例一: 打印hello systemtap

以root用户或者具有sudo权限的用户运行以下命令:

$stap -ve 'probe begin { log("hello systemtap!") exit() }'
  
如果安装正确,会得到如下类似的输出结果:

Pass 1: parsed user script and 96 library script(s) using 55100virt/26224res/2076shr/25172data kb, in 120usr/0sys/119real ms.
  
Pass 2: analyzed script: 1 probe(s), 2 function(s), 0 embed(s), 0 global(s) using 55496virt/27016res/2172shr/25568data kb, in 0usr/0sys/4real ms.
  
Pass 3: translated to C into "/tmp/stapYqNuF9/stap_e2d1c1c9962c809ee9477018c642b661_939_src.c" using 55624virt/27380res/2488shr/25696data kb, in 0usr/0sys/0real ms.
  
Pass 4: compiled C into "stap_e2d1c1c9962c809ee9477018c642b661_939.ko" in 1230usr/160sys/1600real ms.
  
Pass 5: starting run.
  
hello systemtap!
  
Pass 5: run completed in 0usr/10sys/332real ms.
  
示例二: 打印4s内所有open系统调用的信息

创建systemtap脚本文件test2.stp:

# !/usr/bin/stap

probe begin
  
{

log("begin to probe")
  
}

probe syscall.open
  
{

printf ("%s(%d) open (%s)\n", execname(), pid(), argstr)
  
}

probe timer.ms(4000) # after 4 seconds
  
{

exit ()
  
}

probe end
  
{

log("end to probe")
  
}
  
将该脚本添加可执行的权限 chmod +x test2.stp ,使用./test2.stp 运行该脚本,即可打印4s内所有open系统调用的信息,打印格式为: 进程名 (进程号) 打开什么文件。 大家可以自行去测试,如果两个示例都能正确运行,基本上算是安装成功了！

systemtap 工作原理
  
systemtap 的核心思想是定义一个事件 (event) ,以及给出处理该事件的句柄 (Handler) 。当一个特定的事件发生时,内核运行该处理句柄,就像快速调用一个子函数一样,处理完之后恢复到内核原始状态。这里有两个概念:

事件 (Event) : systemtap 定义了很多种事件,例如进入或退出某个内核函数、定时器时间到、整个systemtap会话启动或退出等等。
  
句柄 (Handler) : 就是一些脚本语句,描述了当事件发生时要完成的工作,通常是从事件的上下文提取数据,将它们存入内部变量中,或者打印出来。
  
Systemtap 工作原理是通过将脚本语句翻译成C语句,编译成内核模块。模块加载之后,将所有探测的事件以钩子的方式挂到内核上,当任何处理器上的某个事件发生时,相应钩子上句柄就会被执行。最后,当systemtap会话结束之后,钩子从内核上取下,移除模块。整个过程用一个命令 stap 就可以完成。 上面只是简单的原理,更多背后的机理参考网上资料和相应的论文。 图 systemtap 处理流程

更多参考
  
systemtap 官网给出了自学教程及相关论文,选择看这个已经足够了: <https://sourceware.org/systemtap/documentation.html>
  
IBM 编写的systemtap 指南也是很不错的:  <http://www.redbooks.ibm.com/abstracts/redp4469.html>
