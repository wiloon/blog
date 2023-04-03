---
title: network namespace
author: "-"
date: 2020-07-07 22:35:57
url: /?p=12885
tags:
  - network
categories:
  - inbox
---
## network namespace

network namespace 是实现网络虚拟化的重要功能,它能创建多个隔离的网络空间,它们有独自的网络栈信息。不管是虚拟机还是容器,运行的时候仿佛自己就在独立的网络中。这篇文章介绍 network namespace 的基本概念和用法,network namespace 是 linux 内核提供的功能,这篇文章借助 ip 命令来完成各种操作。ip 命令来自于 iproute2 安装包,一般系统会默认安装,如果没有的话,请读者自行安装。

NOTE: ip 命令因为需要修改系统的网络配置,默认需要 sudo 权限。这篇文章使用 root 用户执行,请不要在生产环境或者重要的系统中用 root 直接执行,以防产生错误。

ip 命令管理的功能很多, 和 network namespace 有关的操作都是在子命令 ip netns 下进行的,可以通过 ip netns help` 查看所有操作的帮助信息。

默认情况下,使用 ip netns 是没有网络 namespace 的,所以 ip netns ls 命令看不到任何输出。
创建 network namespace 也非常简单,直接使用 ip netns add 后面跟着要创建的 namespace 名称。如果相同名字的 namespace 已经存在,命令会报 Cannot create namespace 的错误。

    ip netns add net1
    ip netns ls

ip netns 命令创建的 network namespace 会出现在 /var/run/netns/ 目录下,如果需要管理其他不是 ip netns 创建的 network namespace,只要在这个目录下创建一个指向对应 network namespace 文件的链接就行。

有了自己创建的 network namespace,我们还需要看看它里面有哪些东西。对于每个 network namespace 来说,它会有自己独立的网卡、路由表、ARP 表、iptables 等和网络相关的资源。ip 命令提供了 ip netns exec 子命令可以在对应的 network namespace 中执行命令,比如我们要看一下这个 network namespace 中有哪些网卡。更棒的是,要执行的可以是任何命令,不只是和网络相关的 (当然,和网络无关命令执行的结果和在外部执行没有区别) 。比如下面例子中,执行 bash 命令了之后,后面所有的命令都是在这个 network namespace 中执行的,好处是不用每次执行命令都要把 ip netns exec NAME 补全,缺点是你无法清楚知道自己当前所在的 shell,容易混淆。

ip netns exec 后面跟着 namespace 的名字,比如这里的 net1,然后是要执行的命令,只要是合法的 shell 命令都能运行,比如上面的 ip addr 或者 bash。

每个 namespace 在创建的时候会自动创建一个 lo 的 interface,它的作用和 linux 系统中默认看到的 lo 一样,都是为了实现 loopback 通信。如果希望 lo 能工作,不要忘记启用它:

[root@localhost ~]# ip netns exec net1 ip link set lo up
默认情况下,network namespace 是不能和主机网络,或者其他 network namespace 通信的。

<https://cizixs.com/2017/02/10/network-virtualization-network-namespace/>
